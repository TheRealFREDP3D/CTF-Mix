# CTF Writeup Guidelines

Writing a good CTF writeup is crucial for several reasons:
*   **Learning:** It solidifies your understanding of the techniques used.
*   **Sharing:** It allows you to share knowledge and solutions with the community.
*   **Reference:** It serves as a future reference for yourself or your team.
*   **Portfolio:** It can showcase your skills to potential employers or collaborators.

This document provides guidelines and a suggested structure for creating clear, informative, and reproducible CTF writeups.

## General Principles

1.  **Clarity & Conciseness:** Write clearly and avoid unnecessary jargon. Get straight to the point while providing sufficient detail.
2.  **Reproducibility:** Ensure that someone else could, in theory, follow your steps and arrive at the same result. Include commands used and significant output.
3.  **Logical Flow:** Structure your writeup so that it follows a logical sequence from initial reconnaissance to obtaining the final flag(s).
4.  **Target Audience:** Assume the reader has a basic understanding of CTF concepts but may not be familiar with the specific techniques or tools used in *this* challenge.
5.  **Screenshots:** Use screenshots judiciously. They are helpful for showing complex output, web page layouts, or visual elements of an exploit. Ensure they are clear and relevant. Redact any sensitive information.
6.  **Flag Format:** Clearly state the flag format found (e.g., `HTB{...}`, `flag{...}`) and where the flags were located.

## Suggested Structure

### 1. Challenge Information
*   **Name:** The name of the challenge.
*   **Category:** (e.g., Web, Crypto, Pwn, Reverse Engineering, Forensics, Misc).
*   **Platform:** (e.g., HackTheBox, TryHackMe, CTFd instance name).
*   **Points:** (If applicable).
*   **Difficulty (Your Rating):** (e.g., Easy, Medium, Hard).
*   **Description:** The official challenge description provided by the organizers.

### 2. Initial Analysis / Reconnaissance
*   Describe the initial steps taken (e.g., reading the description, downloading files, examining network traffic, running basic tools).
*   Detail any information gathered during this phase (e.g., open ports from `nmap`, file types from `file`, strings from a binary).

### 3. Solution Path
Break this down into clear phases, often corresponding to how the challenge is designed or how flags are obtained.

#### Example Phases:
*   **Information Gathering / Enumeration:** Detail service enumeration, directory busting, version identification, etc.
*   **Exploitation:** Explain the vulnerability found, the steps taken to exploit it, and the tools or scripts used. Include relevant commands and snippets of output.
*   **Privilege Escalation (if applicable):** If the challenge involves gaining higher privileges (e.g., from user to root), detail this process.
*   **Flag Retrieval:** Show exactly where and how the flag was found.

Use subheadings liberally to organize this section.

### 4. Key Learnings / Takeaways
*   Summarize the main concepts or techniques learned or reinforced by solving this challenge.
*   Mention any pitfalls encountered and how they were overcome.
*   Highlight any interesting or novel aspects of the challenge or solution.

### 5. Conclusion
*   Briefly summarize the overall experience.
*   State whether the challenge was enjoyable or frustrating, and why.

### 6. Appendix (Optional but useful)
*   **Full Commands Log:** A more comprehensive list of commands run, potentially copy-pasteable.
*   **Code / Scripts:** Include the full code of any custom scripts written for the challenge.
*   **References:** Link to any external resources, documentation, or previous writeups that were helpful.

## Tips

*   **Write as you go (or soon after):** It's easier to document the process while it's fresh in your mind.
*   **Use a template:** Consider using or adapting the note-taking template (`Note-Template/DRAFT-CTFs-Notes-Template-Obsidian.md`) as a base for your writeup structure.
*   **Proofread:** Check for grammatical errors and clarity before publishing.
*   **Be Ethical:** Do not publish writeups for active challenges. Respect the rules of the platform and the effort of the organizers.