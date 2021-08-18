export default {
  GET_STOCKS: (s) => {
    return s.list_stoks || []
  },
  GET_PORTFOLIO: (s) => {
    return s.portfolio || []
  },
  GET_CANDLES: (s) => {
    return [{
      data: s.candles.map(
        (candle) => {
          return [Date.parse(candle.date), [candle.open, candle.high, candle.low, candle.close].map(price => (price.toFixed(2)))]
        }
      ) || []
    }]
  },
  GET_LINE_GRAPH: (s) => {
    return [{
      data: s.candles.map(
        (candle) => {
          return [candle.date, candle.close.toFixed(2)]
        }
      ) || []
    }]
  },
  GET_PORTFOLIO_SUMM: (s) => {
    let summ = 0
    for (const item of s.portfolio) {
      summ += item.aver_price * item.count
    }
    return summ
  },
  GET_ORDERS: (s) => {
    const list = s.orders
    const res = []
    for (const item of list) {
      if (item.is_closed) {
        const date = new Date(item.date_closed)
        const d = [
          '0' + date.getDate(),
          '0' + (date.getMonth() + 1),
          '' + date.getFullYear()
        ].map(component => component.slice(-2)).slice(0, 3).join('.')
        if ((res.length !== 0) && (d === res[res.length - 1].date)) {
          res[res.length - 1].orders.push(item)
        } else {
          res.push({
            date: d,
            orders: [item]
          })
        }
      }
    }
    return res
  },
  GET_ORDERS_ACTIVE: (s) => {
    const list = s.orders
    const res = []
    for (const item of list) {
      if (!item.is_closed) {
        res.push(item)
      }
    }
    return res
  }
}
