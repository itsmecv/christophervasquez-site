---
title: Four Surprising Uses For Cryptography - Part 4: Non-repudiation
date: 2020-02-03
---

I've been studying [CISSP](https://en.wikipedia.org) materials ([turns out I passed](https://www.linkedin.com). Yay!), and this series is an attempt to synthesize my studies and notes into something consumable. I hope that it helps you as much as it helped me cement my own understanding. If you haven't read the earlier parts of this series, you might want to check them out first:

## Part 4: Non-repudiation

Non-repudiation - ensuring proof that a specific actor took action

We can use cryptography to to prove that some actor took a specific action, and that actor can't reject, or "repudiate" that they took the action. This is more important than you may first realize.

It is very important to be able to prove an actor said or agreed to something. In the old days, we would use signatures to do this. You would sign a check to prove you agreed to transfer funds from your bank account to the grocery store, or you might sign a contract to prove that you agreed to it. If the contract signee repudiated, or asserted that it was never them who agreed, they could be taken to court and proven that their signature was in fact authentic. Today, we transact, contract, and generally do business remotely via the internet. We can instead provide non-repudiation via encryption.

Asymmetric Encryption

The math behind asymmetric encryption is beyond the scope of this article, but Wikipedia has a [somewhat understandable example on the page for RSA](https://en.wikipedia.org), one of the most widely used encryption algorithms. Here's the important bit to understand: With some neat math, we can make a private and public key.

- Public Key - a number that you allow everyone to see to use for encryption. It can be used to decrypt data that was encrypted with the private key.

- Private Key - a number that you keep secret and use for encryption yourself. It can be used to decrypt data that was encrypted with the public key.

These keys are a pair of numbers that have a special relationship to each other. If some information is encrypted with one of these keys, it can only be decrypted with the other key. One key should be kept private known only to one's self, and the other can be published for all the world to see.

Now, let's imagine that Alice wants to agree to a contract with Bob. They both want to ensure that it can be proven in a court of law that they both agreed to the contract terms. They want to do this over the internet because they don't live near each other. They can use encryption.

All they have to do is keep their private keys secret, post their public key somewhere everyone can see ([PKI](https://en.wikipedia.org) is used for this, but that's a topic for another time) and encrypt a small message like "I agree to this contract" with their private keys.

![four-surprising-uses-for-cryptography-part-4-non-repudiation image 0](../assets/four-surprising-uses-for-cryptography-part-4-non-repudiation-0.png)

A picture describing non-repudiation with asymmetric Cryptography

Because of the special mathematical relationship between the private and public keys, we have irrefutable mathematical proof that only someone in possession of the private keys could have agreed to the contract.
