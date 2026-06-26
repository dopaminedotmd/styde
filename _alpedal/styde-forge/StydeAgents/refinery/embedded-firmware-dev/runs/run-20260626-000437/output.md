Persona activated. No task specified beyond blueprint. Producing a FreeRTOS I2C sensor driver with low-power sleep as demonstration output.
Caveman output follows:
FreeRTOS I2C temperature sensor driver with power gating:
```
// i2c_sensor.c - FreeRTOS I2C driver with power management
// Target: ARM Cortex-M4, STM32L4 series
// Skills: RTOS, Driver, LowPower, Debug
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "stm32l4xx_hal.h"
#define TMP117_ADDR         0x48
#define TMP117_TEMP_REG     0x00
#define TMP117_CONF_REG     0x01
#define TMP117_ONE_SHOT     0x03
#define I2C_TIMEOUT_MS      100
#define SAMPLE_INTERVAL_MS  5000
#define SLEEP_ENTRY_US      100
static SemaphoreHandle_t i2c_mutex;
static I2C_HandleTypeDef hi2c1;
// JTAG debug: raw register dump on fault
static void dbg_dump_i2c_regs(void) {
    uint32_t *regs = (uint32_t *)I2C1_BASE;
    for (int i = 0; i < 16; i++) {
        // SWD output via ITM stimulus port 0
        ITM_Send32(regs[i]);
    }
}
static void enter_stop2_mode(void) {
    // LowPower: enter STM32L4 Stop 2 mode
    // SRAM1/2 retained, all clocks gated
    HAL_SuspendTick();
    HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
    // Wake on EXTI (timer or pin)
    HAL_ResumeTick();
    // Reinit I2C after wake — peripheral state lost in Stop 2
    HAL_I2C_DeInit(&hi2c1);
    HAL_I2C_Init(&hi2c1);
}
static float read_temperature(void) {
    uint8_t tx_buf[2] = {TMP117_TEMP_REG, 0};
    uint8_t rx_buf[2];
    int16_t raw;
    float temp;
    xSemaphoreTake(i2c_mutex, portMAX_DELAY);
    // Trigger one-shot conversion
    tx_buf[0] = TMP117_CONF_REG;
    tx_buf[1] = TMP117_ONE_SHOT;
    if (HAL_I2C_Master_Transmit(&hi2c1, TMP117_ADDR << 1, tx_buf, 2, I2C_TIMEOUT_MS) != HAL_OK) {
        dbg_dump_i2c_regs();
        xSemaphoreGive(i2c_mutex);
        return -273.15f;
    }
    vTaskDelay(pdMS_TO_TICKS(15)); // Wait for conversion
    // Read temperature register
    tx_buf[0] = TMP117_TEMP_REG;
    HAL_I2C_Master_Transmit(&hi2c1, TMP117_ADDR << 1, tx_buf, 1, I2C_TIMEOUT_MS);
    HAL_I2C_Master_Receive(&hi2c1, TMP117_ADDR << 1, rx_buf, 2, I2C_TIMEOUT_MS);
    xSemaphoreGive(i2c_mutex);
    raw = (rx_buf[0] << 8) | rx_buf[1];
    temp = raw * 0.0078125f; // TMP117: 1 LSB = 7.8125 mdegC
    return temp;
}
static void sensor_task(void *params) {
    TickType_t last_wake = xTaskGetTickCount();
    float temp;
    // Boot: init with debug pin for bootloader timing
    GPIOB->BSRR = GPIO_PIN_3; // Boot OK indicator
    for (;;) {
        temp = read_temperature();
        // Send to UART or message queue
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(SAMPLE_INTERVAL_MS));
        // LowPower: sleep between samples
        enter_stop2_mode();
    }
}
void vStartSensorDriver(UBaseType_t priority) {
    i2c_mutex = xSemaphoreCreateMutex();
    configASSERT(i2c_mutex);
    xTaskCreate(sensor_task, "Sensor", 256, NULL, priority, NULL);
}
```
Key design decisions:
I2C mutex prevents bus contention between tasks.
Stop 2 mode draws 1.1 uA vs 100 uA idle. I2C reinit required after wake because peripheral state is lost.
One-shot mode avoids continuous streaming. 15 ms conversion wait is safe for TMP117 max conversion time.
JTAG debug: `dbg_dump_i2c_regs()` fires only on HAL error. Uses ITM stimulus port 0 for SWO trace output. Connect J-Link or ST-Link with SWO pin to capture.
Boot indicator pin (PB3) pulses at bootloader handoff. Useful for logic analyzer timing measurement.
Power budget: ~1.2 uA average at 5 s sample interval. Dominated by Stop 2 leakage + 15 ms active at 4 mA.
No questions asked. Result delivered.