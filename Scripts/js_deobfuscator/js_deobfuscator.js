#!/usr/bin/env node
/**
 * JS Deobfuscator - Generic tool for decoding obfuscated JavaScript
 * 
 * Handles the common pattern:
 *   1. String array function (returns array of encoded strings)
 *   2. Rotation IIFE (shuffles array until a numeric condition matches)
 *   3. Decoder function (looks up index in rotated array, may apply transforms)
 *   4. Business logic (calls decoder via alias to get strings at runtime)
 *   5. Function declarations (hoisted, available everywhere)
 *
 * Usage: node js_deobfuscator.js <input.js> [output.js]
 */

const fs = require('fs');
const vm = require('vm');

// ─── Configuration ────────────────────────────────────────────────────────────
const TIMEOUT_MS = 15000;
const MAX_STRING_LEN = 2000;

// ─── CLI ──────────────────────────────────────────────────────────────────────
const inputFile = process.argv[2];
if (!inputFile) {
    console.error('Usage: node js_deobfuscator.js <input.js> [output.js]');
    process.exit(1);
}
const outputFile = process.argv[3] || inputFile.replace(/\.js$/, '.deobfuscated.js');

const source = fs.readFileSync(inputFile, 'utf8');
console.log(`[*] Read ${source.length} bytes from ${inputFile}`);

// ─── Helper: Extract balanced braces from a string ────────────────────────────
function extractBalanced(str, startPos) {
    let brace = 0, started = false;
    for (let i = startPos; i < str.length; i++) {
        if (str[i] === '{') { brace++; started = true; }
        else if (str[i] === '}') { brace--; if (started && brace === 0) return i + 1; }
    }
    return -1;
}

// ─── Helper: Extract balanced parens from a string (string-aware) ─────────────
function extractBalancedParens(str, startPos) {
    let paren = 0, inString = false, stringChar = null, escapeNext = false;
    for (let i = startPos; i < str.length; i++) {
        const c = str[i];
        if (escapeNext) { escapeNext = false; continue; }
        if (c === '\\' && inString) { escapeNext = true; continue; }
        if (inString) { if (c === stringChar) inString = false; continue; }
        if (c === '"' || c === "'" || c === '`') { inString = true; stringChar = c; continue; }
        if (c === '(') paren++;
        else if (c === ')') { paren--; if (paren === 0) return i; }
    }
    return -1;
}

// ─── Phase 1: Parse file structure ────────────────────────────────────────────
console.log('\n[*] Phase 1: Parsing file structure...');

// Find all function declarations
const funcDeclRegex = /function\s+(\w+)\s*\(/g;
const functionDecls = {};
let match;
while ((match = funcDeclRegex.exec(source)) !== null) {
    const name = match[1];
    const pos = match.index;
    const bodyStart = source.indexOf('{', pos);
    if (bodyStart === -1) continue;
    const bodyEnd = extractBalanced(source, bodyStart);
    if (bodyEnd === -1) continue;
    functionDecls[name] = { pos, body: source.substring(pos, bodyEnd) };
}
console.log(`  Found ${Object.keys(functionDecls).length} function declarations: ${Object.keys(functionDecls).join(', ')}`);

// ─── Phase 2: Identify components ─────────────────────────────────────────────
console.log('\n[*] Phase 2: Identifying components...');

let stringArrayFunc = null;
let decoderFunc = null;

for (const [name, decl] of Object.entries(functionDecls)) {
    // String array: contains array literal return or recursive return
    if (decl.body.includes('return [') || decl.body.match(/return\s+\w+\(\);/)) {
        if (decl.body.includes("'") || decl.body.includes('"')) {
            if (!stringArrayFunc || decl.body.length > functionDecls[stringArrayFunc].body.length) {
                stringArrayFunc = name;
            }
        }
    }
    // Decoder: contains idx-hex offset + array indexing
    if ((decl.body.match(/=\s*\w+\s*-\s*0x[0-9a-f]+/) || decl.body.match(/\[\s*\w+\s*-\s*0x[0-9a-f]+\s*\]/))
        && decl.body.includes('return') && decl.body.length > 200) {
        if (!decoderFunc) decoderFunc = name;
    }
}
console.log(`  String array function: ${stringArrayFunc || 'unknown'}`);
console.log(`  Decoder function: ${decoderFunc || 'unknown'}`);

// ─── Phase 3: Extract rotation IIFE ───────────────────────────────────────────
console.log('\n[*] Phase 3: Extracting rotation IIFE...');

let rotationIIFE = null;
let rotationEnd = -1;

// The file structure may be:
//   (rotationIIFE, businessLogicIIFE()); function ...; function ...
// OR:
//   rotationIIFE; businessLogicIIFE(); function ...
//
// Strategy 1: Find the rotation IIFE by its ending pattern
// The rotation IIFE typically ends with: }(stringArrayFunc,0xNNNNN)
if (stringArrayFunc) {
    const endPattern = new RegExp(`}\\(${stringArrayFunc},0x[0-9a-f]+\\)`);
    const endMatch = source.match(endPattern);
    if (endMatch) {
        // The rotation IIFE is from start to end of this pattern
        // But it may be wrapped in outer parens as part of a comma expression
        const rawEnd = endMatch.index + endMatch[0].length;
        
        // Check if this is inside a comma expression: (rotIIFE, bizIIFE())
        // The rotation IIFE itself may start with ( or without
        let rotStart = 0;
        let rotText = source.substring(rotStart, rawEnd);
        
        // Check if the text before the rotation IIFE is just (
        // and the text after is , then another expression
        if (rawEnd < source.length && source[rawEnd] === ',') {
            // This is a comma expression. The rotation IIFE is the first expression.
            // It may be wrapped in () or not.
            // If the file starts with (function(, the ( at pos 0 is the outer wrapper
            // and the rotation IIFE is actually the inner expression
            
            // Check if the rotation IIFE needs to be wrapped
            // by testing if it's valid JS as-is
            const testCode = rotText;
            try {
                new Function(testCode); // Quick syntax check
                rotationIIFE = testCode;
            } catch (e) {
                // Not valid - try wrapping in ()
                try {
                    new Function('(' + testCode + ')');
                    rotationIIFE = '(' + testCode + ')';
                } catch (e2) {
                    // Still not valid - the rotation IIFE might start later
                    // Find the actual function( inside
                    const funcStart = rotText.indexOf('function(');
                    if (funcStart !== -1 && funcStart > 0) {
                        const innerRot = '(' + rotText.substring(funcStart) + ')';
                        try {
                            new Function(innerRot);
                            rotationIIFE = innerRot;
                            rotStart = funcStart;
                        } catch (e3) {
                            console.log(`  Warning: Could not parse rotation IIFE`);
                        }
                    }
                }
            }
            
            if (rotationIIFE) {
                rotationEnd = rawEnd;
                console.log(`  Found rotation IIFE via ending pattern, length ${rotationIIFE.length}`);
            }
        } else {
            // Not a comma expression - rotation IIFE is standalone
            rotationIIFE = rotText;
            rotationEnd = rawEnd;
            console.log(`  Found rotation IIFE (standalone), length ${rotationIIFE.length}`);
        }
    }
}

// Strategy 2: If file starts with (function(, extract the first expression
if (!rotationIIFE && source.startsWith('(function(')) {
    // Find the end of the first expression by looking for the comma
    // Pattern: (function(...){...}(args)),(function...
    const commaPattern = /\}\([^)]*\)\),\(function/;
    const commaMatch = source.match(commaPattern);
    if (commaMatch) {
        // The rotation IIFE ends just before the comma
        const rotEndIdx = commaMatch.index + commaMatch[0].indexOf('),(');
        rotationIIFE = source.substring(0, rotEndIdx + 1); // include the )
        rotationEnd = rotEndIdx + 1;
        console.log(`  Found rotation IIFE via comma pattern, length ${rotationIIFE.length}`);
    }
}

// Determine where business logic starts
let businessStart = rotationEnd;
if (rotationEnd > 0 && source[rotationEnd] === ',') {
    businessStart = rotationEnd + 1; // skip comma
    console.log(`  Comma expression detected, business logic starts at ${businessStart}`);
}

if (!rotationIIFE) {
    console.log(`  No rotation IIFE found (strings may not be rotated)`);
}

// ─── Phase 4: Find decoder aliases ────────────────────────────────────────────
console.log('\n[*] Phase 4: Finding decoder aliases...');

// Search the entire source for assignments of the decoder function
const aliasRegex = new RegExp(`(\\w+)\\s*=\\s*${decoderFunc}\\s*[;,]`, 'g');
const aliases = [];
while ((match = aliasRegex.exec(source)) !== null) {
    aliases.push({ name: match[1], pos: match.index });
}
// Also check for: var X = decoderFunc (no semicolon, part of comma expression)
const aliasRegex2 = new RegExp(`(\\w+)\\s*=\\s*${decoderFunc}\\s*,`, 'g');
while ((match = aliasRegex2.exec(source)) !== null) {
    if (!aliases.find(a => a.name === match[1])) {
        aliases.push({ name: match[1], pos: match.index });
    }
}

const decoderNames = [decoderFunc, ...aliases.map(a => a.name)].filter(Boolean);
console.log(`  Decoder aliases: ${aliases.map(a => a.name).join(', ') || 'none'}`);
console.log(`  All decoder references: ${decoderNames.join(', ')}`);

// ─── Phase 5: Execute setup code in sandbox ───────────────────────────────────
console.log('\n[*] Phase 5: Executing setup code in VM sandbox...');

function buildSandbox() {
    const noop = () => {};
    const proxy = new Proxy(noop, {
        apply: (t, thisArg, args) => proxy,
        get: (t, prop) => {
            if (prop === Symbol.toPrimitive) return () => '';
            return proxy;
        }
    });
    const domProxy = new Proxy({}, {
        get: (target, prop) => {
            if (typeof prop === 'symbol') return undefined;
            if (prop === 'cookie') return '';
            if (prop === 'createElement') return () => ({
                style: proxy, setAttribute: noop, addEventListener: noop,
                classList: { add: noop, remove: noop, contains: () => false },
                appendChild: noop, innerHTML: '', src: '', href: ''
            });
            if (prop === 'getElementsByTagName') return () => [];
            if (prop === 'querySelector') return () => null;
            if (prop === 'querySelectorAll') return () => [];
            if (prop === 'addEventListener') return noop;
            if (prop === 'getElementById') return () => null;
            if (prop === 'createTextNode') return () => ({});
            if (prop === 'createDocumentFragment') return () => ({ appendChild: noop, querySelectorAll: () => [] });
            return proxy;
        }
    });
    return {
        window: domProxy, self: domProxy, top: domProxy, parent: domProxy,
        frames: domProxy, globalThis: domProxy, document: domProxy,
        navigator: { userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' },
        location: new Proxy({ href: 'https://example.com/', hostname: 'example.com', protocol: 'https:' }, {
            get: (t, p) => p === Symbol.toPrimitive ? t.href : t[p]
        }),
        console, setTimeout, setInterval, clearTimeout, clearInterval,
        parseInt, parseFloat, isNaN, isFinite,
        encodeURIComponent, decodeURIComponent, encodeURI, decodeURI,
        escape, unescape,
        btoa: s => Buffer.from(String(s), 'binary').toString('base64'),
        atob: s => Buffer.from(String(s), 'base64').toString('binary'),
        Array, Object, String, Number, Boolean, Math, Date, RegExp, Error,
        TypeError, RangeError, SyntaxError, ReferenceError, URIError, EvalError,
        Map, Set, WeakMap, WeakSet, Promise, Symbol, Proxy, Reflect,
        DataView, ArrayBuffer, SharedArrayBuffer,
        Uint8Array, Uint16Array, Uint32Array, Int8Array, Int16Array, Int32Array,
        Float32Array, Float64Array, BigInt, BigInt64Array, BigUint64Array,
        TextEncoder: class { encode() { return new Uint8Array(0); } },
        TextDecoder: class { decode() { return ''; } },
        crypto: {
            subtle: new Proxy({}, { get: () => async () => new Uint8Array(16) }),
            getRandomValues: arr => { for (let i = 0; i < arr.length; i++) arr[i] = Math.floor(Math.random() * 256); return arr; }
        },
        fetch: async (url) => {
            console.log(`  [FETCH] ${url}`);
            return { json: async () => ({}), text: async () => '', ok: false, status: 404, headers: { get: () => null } };
        },
        performance: { now: () => Date.now() },
        sessionStorage: new Proxy({}, { get: () => noop }),
        localStorage: new Proxy({}, { get: () => noop }),
        alert: noop, confirm: () => false, prompt: () => '',
        history: new Proxy({}, { get: () => noop }),
        MutationObserver: class { observe() {} disconnect() {} },
        IntersectionObserver: class { observe() {} disconnect() {} },
        ResizeObserver: class { observe() {} disconnect() {} },
        requestAnimationFrame: fn => setTimeout(fn, 0),
        cancelAnimationFrame: id => clearTimeout(id),
        Image: class { set src(v) {} },
        XMLHttpRequest: class { open() {} send() {} setRequestHeader() {} addEventListener() {} },
    };
}

// Build setup code: function declarations (hoisted) + rotation IIFE
let setupCode = '';
for (const [name, decl] of Object.entries(functionDecls)) {
    setupCode += decl.body + '\n';
}
if (rotationIIFE) {
    setupCode += rotationIIFE + ';\n';
}

const sandbox = buildSandbox();
const ctx = vm.createContext(sandbox);

try {
    vm.runInContext(setupCode, ctx, { timeout: TIMEOUT_MS });
    console.log('  Setup code executed successfully');
} catch (e) {
    console.error(`  Setup execution error: ${e.message.substring(0, 200)}`);
    // Try without rotation IIFE
    if (rotationIIFE) {
        console.log('  Retrying without rotation IIFE...');
        let setupCode2 = '';
        for (const [name, decl] of Object.entries(functionDecls)) {
            setupCode2 += decl.body + '\n';
        }
        const ctx2 = vm.createContext(buildSandbox());
        try {
            vm.runInContext(setupCode2, ctx2, { timeout: TIMEOUT_MS });
            console.log('  Setup (without rotation) executed successfully');
            // Use this context instead
            Object.assign(ctx, ctx2);
        } catch (e2) {
            console.error(`  Setup (without rotation) also failed: ${e2.message.substring(0, 200)}`);
        }
    }
}

// ─── Phase 6: Build decoder call map ──────────────────────────────────────────
console.log('\n[*] Phase 6: Building decoder call map...');

// Build regex pattern that matches calls to ANY decoder name
const allDecoderNames = decoderNames.map(n => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
const callPattern = new RegExp(`(${allDecoderNames.join('|')})\\s*\\(\\s*(0x[0-9a-fA-F]+|\\d+)\\s*,\\s*['"]([^'"]+)['"]\\s*\\)`, 'g');

const callMap = new Map(); // "idx,key" -> decoded value
const allCalls = [];
let callMatch;

while ((callMatch = callPattern.exec(source)) !== null) {
    const fullMatch = callMatch[0];
    const idx = parseInt(callMatch[1 + 1], 16) || parseInt(callMatch[1 + 1], 10);
    const key = callMatch[1 + 2];
    const mapKey = `${idx},${key}`;

    if (!callMap.has(mapKey)) {
        try {
            const decodeScript = `var result = ${decoderFunc}(${idx}, '${key.replace(/'/g, "\\'")}'); result;`;
            const decoded = vm.runInContext(decodeScript, ctx, { timeout: 1000 });
            if (typeof decoded === 'string' && decoded.length <= MAX_STRING_LEN) {
                callMap.set(mapKey, decoded);
            } else {
                callMap.set(mapKey, null);
            }
        } catch (e) {
            callMap.set(mapKey, null);
        }
    }

    allCalls.push({ fullMatch, idx, key, mapKey, pos: callMatch.index });
}

const decodedCount = [...callMap.values()].filter(v => v !== null).length;
console.log(`  Found ${allCalls.length} total decoder calls`);
console.log(`  ${decodedCount} unique decoded strings`);

// Show some decoded strings as preview
const preview = [...callMap.entries()].filter(([k, v]) => v !== null).slice(0, 10);
if (preview.length > 0) {
    console.log('  Sample decoded strings:');
    for (const [k, v] of preview) {
        console.log(`    ${k} => ${JSON.stringify(v).substring(0, 80)}`);
    }
}

// ─── Phase 7: Replace decoder calls in source ─────────────────────────────────
console.log('\n[*] Phase 7: Replacing decoder calls...');

let result = source;
const sortedCalls = [...allCalls].sort((a, b) => b.pos - a.pos);

let replaced = 0, skipped = 0;
for (const call of sortedCalls) {
    const decoded = callMap.get(call.mapKey);
    if (decoded !== null && decoded !== undefined) {
        const replacement = JSON.stringify(decoded);
        result = result.substring(0, call.pos) + replacement + result.substring(call.pos + call.fullMatch.length);
        replaced++;
    } else {
        skipped++;
    }
}
console.log(`  Replaced ${replaced} calls, skipped ${skipped}`);

// ─── Phase 8: Remove rotation IIFE and string array function ──────────────────
console.log('\n[*] Phase 8: Cleaning up dead code...');

// Remove rotation IIFE and everything before business logic
if (rotationIIFE && businessStart > 0) {
    // The rotation IIFE was replaced with decoded strings, so find where business logic starts
    // by looking for the business logic IIFE pattern
    const bizPattern = /\(function\s*\(\s*\)\s*\{/;
    const bizMatch = result.match(bizPattern);
    if (bizMatch) {
        const bizIdx = result.indexOf(bizMatch[0]);
        // Remove everything before the business logic IIFE
        // But keep any leading whitespace/newlines
        let removeEnd = bizIdx;
        // Also remove trailing , or ) that might be left over
        while (removeEnd > 0 && (result[removeEnd - 1] === ',' || result[removeEnd - 1] === ')' || result[removeEnd - 1] === ';')) {
            removeEnd--;
        }
        result = result.substring(removeEnd);
        console.log(`  Removed rotation IIFE and prefix (${removeEnd} chars)`);
    } else {
        console.log(`  Warning: Could not find business logic IIFE pattern`);
    }
}

// Remove string array function (no longer needed)
if (stringArrayFunc && functionDecls[stringArrayFunc]) {
    const arrBody = functionDecls[stringArrayFunc].body;
    // Find it in the result (may have shifted due to replacements)
    // Use the function name to find it
    const funcPattern = new RegExp(`function\\s+${stringArrayFunc}\\s*\\(`);
    const funcMatch = result.match(funcPattern);
    if (funcMatch) {
        const funcStart = result.indexOf(funcMatch[0]);
        const funcEnd = extractBalanced(result, result.indexOf('{', funcStart));
        if (funcEnd !== -1) {
            result = result.substring(0, funcStart) + result.substring(funcEnd);
            console.log(`  Removed string array function '${stringArrayFunc}'`);
        }
    }
}

// ─── Phase 9: Basic beautification ────────────────────────────────────────────
console.log('\n[*] Phase 9: Beautifying...');

// Add newlines after semicolons and braces (basic formatting)
result = result.replace(/;(?=\s*(var|let|const|function|if|else|for|while|return|switch|case|break|continue|throw|try|catch|finally|new|delete|typeof|instanceof|void|do|with))\s*/g, ';\n');
result = result.replace(/\}(?=\s*(function|var|let|const|if|else|for|while|return|switch|case|break|continue|throw|try|catch|finally|new|\}))\s*/g, '}\n');
result = result.replace(/\{(?=\s*(var|let|const|function|if|else|for|while|return|switch|case|break|continue|throw|try|catch|finally|new|\w+\s*[=:]))\s*/g, '{\n');

// ─── Write output ─────────────────────────────────────────────────────────────
fs.writeFileSync(outputFile, result);
console.log(`\n[+] Deobfuscated output written to ${outputFile}`);
console.log(`    Input: ${source.length} bytes -> Output: ${result.length} bytes`);

// ─── Summary of decoded strings ───────────────────────────────────────────────
console.log('\n=== DECODED STRINGS SUMMARY ===');
const decodedStrings = [...callMap.entries()]
    .filter(([k, v]) => v !== null)
    .sort((a, b) => a[1].localeCompare(b[1]));

const categories = {
    urls: [], fetches: [], dom: [], crypto: [], storage: [],
    strings: [], numbers: [], other: []
};

for (const [key, val] of decodedStrings) {
    if (val.match(/^https?:\/\//)) categories.urls.push(val);
    else if (val.match(/^(GET|POST|PUT|DELETE|PATCH|HEAD)/i)) categories.fetches.push(val);
    else if (val.match(/^(cookie|session|localStorage|sessionStorage|document|window|body|div|span|input|form|class|id|style|src|href)/i)) categories.dom.push(val);
    else if (val.match(/^(aes|sha|pbkdf|encrypt|decrypt|key|iv|salt|hash)/i)) categories.crypto.push(val);
    else if (val.match(/^(set|get|remove|clear)(Item|Cookie)?$/i)) categories.storage.push(val);
    else if (/^\d+$/.test(val)) categories.numbers.push(val);
    else categories.strings.push(val);
}

if (categories.urls.length > 0) {
    console.log(`\nURLs (${categories.urls.length}):`);
    categories.urls.forEach(s => console.log(`  ${s}`));
}
if (categories.fetches.length > 0) {
    console.log(`\nFetch/API (${categories.fetches.length}):`);
    categories.fetches.forEach(s => console.log(`  ${s}`));
}
if (categories.crypto.length > 0) {
    console.log(`\nCrypto (${categories.crypto.length}):`);
    categories.crypto.forEach(s => console.log(`  ${s}`));
}
if (categories.storage.length > 0) {
    console.log(`\nStorage (${categories.storage.length}):`);
    categories.storage.forEach(s => console.log(`  ${s}`));
}
if (categories.dom.length > 0) {
    console.log(`\nDOM (${categories.dom.length}):`);
    categories.dom.slice(0, 30).forEach(s => console.log(`  ${s}`));
    if (categories.dom.length > 30) console.log(`  ... and ${categories.dom.length - 30} more`);
}
if (categories.strings.length > 0) {
    console.log(`\nStrings (${categories.strings.length}):`);
    categories.strings.slice(0, 50).forEach(s => console.log(`  ${s}`));
    if (categories.strings.length > 50) console.log(`  ... and ${categories.strings.length - 50} more`);
}
