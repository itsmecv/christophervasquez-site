---
title: Four Surprising Uses For Cryptography - Part 1: Confidentiality
date: 2019-09-13
---

I believe it's important to understand the fundamentals of cybersecurity, and I've been studying CISSP materials to that end. This series is an attempt to synthesize my studies and notes into something consumable. I hope that it helps you as much as it helps me cement my own understanding.

From blockchain to cyber warfare, cryptography is often in the news. The most common understanding of cryptography's utility is to enable confidentiality, but it does much more than that.

Four usages of cryptography:

- Confidentiality - ensuring data is secret to only the individuals intended

- Integrity - ensuring data is not altered without one's knowledge

- Authentication - ensuring one's claimed identity is valid

- Non-repudiation - ensuring proof that a specific actor took action

In this article, I'll cover confidentiality.

Confidentiality

The most commonly thought of uses for cryptography is confidentiality. This is the classic usage of encoding a message with an algorithm before sending it to ensure that anyone intercepting the message in transit can't read the message's meaning. One of the most ubiquitous example of this usage today is [TLS](https://en.wikipedia.org). TLS ensures that the data your browser sends to a web server can't be read by someone intercepting that data.

A more understandable and oft-cited example of cryptography usage for confidentiality is the [Caeser Cypher](https://en.wikipedia.org). The Caeser Cypher uses a simple algorithm: It replaces a letter in the alphabet with a letter 3 positions earlier in the alphabet. For example, W would be replaced by T, O would be replaced by L, and so on. "TLOA" encoded with this algorithm, would be decrypted to "WORD."

![four-surprising-uses-for-cryptography-part-1-confidentiality image 0](../assets/four-surprising-uses-for-cryptography-part-1-confidentiality-0.png)

Thanks for riding along. I'll survey the other usages in future posts.
