export default {
  GET_EXchange_MAIN: (s) => {
    return {
      stocks: s.list_stoks || [],
      bonds: [],
      currencies: []
    }
  }
}
