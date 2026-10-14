---
title: A Primer on Parallax Scrolling
date: 2022-04-10
---

I've done a little more game development lately, and one of the first things I did was reimplement parallax scrolling. Reimplementing gave me a newfound appreciation for the technique, and it occurred to me that some folks might not know what parallax scrolling is, or where it game from. So, I thought it might be nice to write a quick primer to share and show off some cool game art in the process.

## What is parallax scrolling?

Parallax scrolling is a technique that tricks the viewer into believing that there is 3d depth to a 2d scene. A scene is composed of multiple layers. Each layer scrolls horizontally in one direction, which gives a sense of movement. Layers that are supposed to be farther from the viewer in the distance scroll slower than layers that are supposed to be closer to the viewer in the foreground. This gives the illusion of depth.

Here is a preview of the layers I've been working with:

And here they are put in motion: ![a-primer-on-parallax-scrolling image 0](../assets/a-primer-on-parallax-scrolling-0.gif)

Parallax scrolling allows us to play with the depth in the scene in subtle ways. The big clouds appear to be farther away because they're scrolling more slowly than the small, faster scrolling clouds. When we combine the layer order with parallax we can get even more playful. The viewer gets a sense that the moon is hung in the atmosphere. The big clouds that are farther away are drifting by at some distance behind the moon, and the smaller clouds which are moving faster are actually transiting in front of the moon. We can show the viewer precisely where the moon is in this fantastical planet's atmosphere with just parallax and layer order.

## Parallax scrolling in history

This was historically applied to film and movies made for a screen, and then later video games. One of the first video games to implement parallax scrolling was Moon Patrol in 1982.

![a-primer-on-parallax-scrolling image 1](../assets/a-primer-on-parallax-scrolling-1.gif)

I can stare at that pixel art scroll in parallax all day...

We can also see parallax scrolling in action in Super Mario World. The geometric mountains in the distance scroll much slower than the ground and trees in the foreground. Though, in my opinion, Mario didn't improve on Moon Patrol's implementation a decade earlier.

![a-primer-on-parallax-scrolling image 2](../assets/a-primer-on-parallax-scrolling-2.gif)

Hopefully you understand parallax scrolling by now, and have enjoyed examples from my own game dev as well as games in history.
