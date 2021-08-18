export default {
  SET_LIST_STOCKS: (state, data) => {
    state.list_stoks = data
  },
  SET_CANDLES: (state, data) => {
    state.candles = data
  },
  SET_STOCK: (state, data) => {
    state.stock = data
  },
  SET_PORTFOLIO: (state, data) => {
    state.portfolio = data
  },
  SET_RATING: (state, data) => {
    state.rating = data
  },
  SET_ORDERS: (state, data) => {
    state.orders = data.sort((a, b) => new Date(b.date_closed) - new Date(a.date_closed))
  }
}
