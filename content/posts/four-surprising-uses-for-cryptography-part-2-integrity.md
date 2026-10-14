---
title: Four Surprising Uses For Cryptography - Part 2: Integrity
date: 2019-09-20
---

I've been studying CISSP materials, and this series is an attempt to synthesize my studies and notes into something consumable. I hope that it helps you as much as it helps me cement my own understanding.

If you haven't read part 1 of this series, you might want to [check it out](four-surprising-uses-for-cryptography-part-1-confidentiality.html) first.

## Part 2: Integrity

Integrity - ensuring data is not altered without one's knowledge

We can use cryptography to check the integrity of data. When integrity measures are in place, we can be sure that...

- a message that was sent wasn't altered before receiving it

- files stored for a long time haven't been altered since we accessed them

- the file we're downloading hasn't been infected with malware since it was uploaded to a website

You can think of a hash as a mathematical thumbprint or digital signature of a piece of data. When we apply a hashing algorithm to a piece of data, it will always generate the same hash. If the data is altered in any way (even adding a space or a period), the hash or "thumbprint" will be different.

![four-surprising-uses-for-cryptography-part-2-integrity image 0](../assets/four-surprising-uses-for-cryptography-part-2-integrity-0.png)

Assuming we receive the hash along with the message in a secure way (there are many fun tricks that cryptosystems use to ensure this, but those are out of scope for this topic) we can compare the message data with the hash by hashing it ourselves with the same algorithm. If we get a different hash, we know the message data has been altered in some way.

## P.S.

When googling for SHA-256 hash calculators I ran across [Daniele Favi's site](https://www.danielefavi.com). In addition to the neat calculator linked above, they have a ton of great blog posts on cryptography, blockchain, and development. Additionally, when editing the HTML of their site to squish the form small enough for a reasonable screenshot size, I stumbled across this GOLDEN joke, and instantly became a fan. Check out Daniele's site and their work. They deserve it.

![four-surprising-uses-for-cryptography-part-2-integrity image 1](../assets/four-surprising-uses-for-cryptography-part-2-integrity-1.png)
