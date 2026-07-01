specificationVersion: 1
title: Monthly Revenue by Product Category
data:
  - month: Jan
    Electronics: 42000
    Apparel: 28000
    HomeGoods: 15000
  - month: Feb
    Electronics: 38500
    Apparel: 32000
    HomeGoods: 16200
  - month: Mar
    Electronics: 51000
    Apparel: 29500
    HomeGoods: 17800
  - month: Apr
    Electronics: 47300
    Apparel: 34100
    HomeGoods: 19200
  - month: May
    Electronics: 52600
    Apparel: 36500
    HomeGoods: 20500
  - month: Jun
    Electronics: 58900
    Apparel: 38800
    HomeGoods: 21300
chart:
  mark: bar
  encoding:
    x:
      field: month
      type: ordinal
      sort: [Jan, Feb, Mar, Apr, May, Jun]
      title: Month
    y:
      field: value
      type: quantitative
      aggregate: sum
      title: Revenue (SEK)
    color:
      field: category
      type: nominal
      scale:
        scheme: tableau10
      title: Category
  layer:
    - transform:
        - fold: [Electronics, Apparel, HomeGoods]
          as: [category, value]
width: 600
height: 400
selection:
    categoryFilter:
        type: multi
        fields: [category]
        bind: legend