export default {
  SET_LIST_STOCKS: (state, data) => {
    state.list_stoks = data
  },
  SET_LIST_STOCKS_UPDATE: (state) => {
    state.list_update = true
  },
  SET_PORTFOLIO: (state, data) => {
    state.portfolio = data
  },
  SET_PORTFOLIO_UPDATE: (state) => {
    state.portfolio_update = true
  }
}
