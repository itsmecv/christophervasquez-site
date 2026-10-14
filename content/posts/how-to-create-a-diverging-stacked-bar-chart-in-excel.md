---
title: How To Create A Diverging Stacked Bar Chart In Excel
date: 2019-04-07
---

Why a diverging stacked bar chart? It's important to use a diverging stacked bar chart in this scenario because I want to illustrate the divergence between the positive and negative responses in user satisfaction Likert data. "Neutral" responses will act as the centerline.

When we get response data it is usually in a format like this: ![how-to-create-a-diverging-stacked-bar-chart-in-excel image 0](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-0.png)

Since we want to center the bars on the Neutral line, we're going to have to split the Neutral values into two columns, each half of the value of Neutral. These columns will represent half of the Neutral dataset on the positive and negative sides of the center line.

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 1](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-1.gif)

We want Extremely dissatisfied, Somewhat dissatisfied, and half of the Neutral values to be plotted to the left of the center line, so we need to make their values negative.

Here's an Excel-Fu Protip: You can quickly change to negative by copying -1 and doing a Paste Special > Multiplication Operation.

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 2](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-2.gif)

In order to ensure our categories are stacked correctly, we need to reverse the order of our negative categories. For example, we want Extremely dissatisfied to be plotted on the extreme left of the center line. If we don't reverse the order, it will be plotted adjacent to the center line.

Excel-Fu Protip: In order to move columns around without replacing values (effectively cutting and inserting the selected column) hold Shift while dragging the edge of the column.

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 3](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-3.gif)

Select all of the data except the original Neutral column and insert a standard stacked bar chart from Insert > Insert Column or Bar Chart > 2D Bar

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 4](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-4.gif)

To fix the Labels, Right Click > Format Axis and change the Label Position to Low.

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 5](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-5.gif)

Now all that's left is to change the colors as you like, ensure the Neutral data are the same color, and delete one of the Neutral Labels.

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 6](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-6.gif)

Edit to your liking and Voila!

![how-to-create-a-diverging-stacked-bar-chart-in-excel image 7](../assets/how-to-create-a-diverging-stacked-bar-chart-in-excel-7.png)
