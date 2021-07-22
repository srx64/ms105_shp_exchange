export default {
  GET_EXchange_MAIN: (s) => {
    return s.list_stoks || []
  },
  GET_PORTFOLIO: (s) => {
    return s.portfolio || []
  },
  GET_PORTFOLIO_SUMM: (s) => {
    let summ = 0
    for (const item of s.portfolio) {
      summ += item.aver_price
    }
    return summ
  }
}
