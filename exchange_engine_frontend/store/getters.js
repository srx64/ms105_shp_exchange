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
  }
}
