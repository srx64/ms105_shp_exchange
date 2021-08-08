<template>
  <section class="ex-info-profile-wrapper">
    <div class="ex-info-profile">
      <div class="container">
        <div class="row" style="width: 100%;justify-content: space-between;">
          <div class="col-auto">
            <div class="ex-info-balance">
              <div class="ex-info-balance-deposit">
                <h6 class="text-h6">
                  Стоимость портфеля
                </h6>
                <div style="display: flex; flex-wrap: wrap;justify-content: space-between;align-items: center;">
                  <div>
                    <h1 class="text-h3">
                      {{ 2000000.6663 | numeral('0,0.00') }} ₮
                    </h1>
                  </div>
                  <div class="pl-8 text-h6">
                    ↑ 1084,12 ₮ (6.42 %)
                  </div>
                </div>
              </div>
              <div class="ex-info-balance-profile mt-5">
                <div>
                  <h6 class="text-h6">
                    Баланс
                  </h6>
                  <div style="display: flex; flex-wrap: wrap;justify-content: space-between;align-items: center;">
                    <div class="balance">
                      <h3 class="text-h4">
                        10,000.00 ₮
                      </h3>
                    </div>
                    <v-btn color="primary" elevation="0">
                      Пополнить
                    </v-btn>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div style="display: none;">
            <div class="row">
              <div class="col-4">
                <div
                  style="background: linear-gradient(180deg, #FFCC00 0%, #FF7A00 100%);
                                        border-radius: 9px;width: 100%;height: 200px;"
                >
                  <h6>Акции</h6>
                </div>
              </div>
              <div class="col-4">
                <div
                  style="background: linear-gradient(180deg, #63CEFE 0%, #5ADDFA 0.01%, #5AC8FA 100%);
                                        border-radius: 9px;width: 100%;height: 200px;"
                >
                  <h6>Облигации</h6>
                </div>
              </div>
              <div class="col-4">
                <div
                  style="background: linear-gradient(180deg, #00A3FF 0%, #0066FF 100%);
                                        border-radius: 9px;width: 100%;height: 200px;"
                >
                  <h6>Валюты</h6>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {

}

</script>

<style>
  .ex-info-profile-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    position: relative;
    top: -12px;
  }

  .ex-info-profile {
    width: 95%;
    height: 100%;
    background: #FFFFFF;
    box-shadow: 0px 5px 15px rgba(217, 217, 217, 0.15);
    border-radius: 0px 0px 15px 15px;
    padding-bottom: 20px;
    padding-top: 20px;
  }

  .ex-info-balance {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
  }

</style>
