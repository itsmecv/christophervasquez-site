---
title: Four Surprising Uses For Cryptography - Part 3: Authentication
date: 2019-11-14
---

I've been studying [CISSP](https://en.wikipedia.org) materials, and this series is an attempt to synthesize my studies and notes into something consumable. I hope that it helps you as much as it helps me cement my own understanding.

If you haven't read the earlier parts of this series, you might want to check them out first:

- [Four Surprising Uses For Cryptography - Part 1: Confidentiality](four-surprising-uses-for-cryptography-part-1-confidentiality.html)

- [Four Surprising Uses For Cryptography - Part 2: Integrity](four-surprising-uses-for-cryptography-part-2-integrity.html)

## Part 3: Authentication

Authentication - ensuring one's claimed identity is valid

We can use cryptography to "authenticate," or check if someone is who they claim to be. A simple example of this is sharing a secret with someone that you'll use to authenticate each other in the future.

Imagine that I'm indoctrinated into the "Skull and Cross Bones" club. The club might share with me a secret with which they'll challenge me when I knock on the clubhouse door. When I knock on the door, the club wants me to use the Caeser Cypher that we discussed in [Four Surprising Uses For Cryptography - Part 1: Confidentiality](four-surprising-uses-for-cryptography-part-1-confidentiality.html) on whatever word or phrase they give me. The process is diagrammed below: ![four-surprising-uses-for-cryptography-part-3-authentication image 0](../assets/four-surprising-uses-for-cryptography-part-3-authentication-0.png)

Since I responded with what the club expected, they can be reasonably sure it is me at the door. This is a simple example of what's known as a Challenge Response Authentication Protocol, or [Challenge-response authentication](https://en.wikipedia.org).

As you can imagine, there are all sorts of problems with the above protocol. What if someone is eavesdropping? They've heard the challenge and response, and can easily deduce the shared secret. There are all sorts of more advanced Challenge Response Authentication Protocols in use today. If you'd like further reading, you can dive into the one used every day in [Open SSH Key Management](https://en.wikipedia.org).
