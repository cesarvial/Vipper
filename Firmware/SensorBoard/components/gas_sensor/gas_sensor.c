#include <stdio.h>
#include "gas_sensor.h"
#include "driver/gpio.h"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

/// @brief Initializes GPIO for reading
/// @param gas_pin = GPIO being configured for receiving digital data of gas sensor 
/// @return 
esp_err_t gas_sensor_init(uint8_t gas_pin){
    gpio_config_t gas_pin_config = {
        .pin_bit_mask = (1ULL << gas_pin),
        .mode = GPIO_MODE_INPUT,
        .pull_down_en = 0,
        .pull_up_en = 0,
        .intr_type = GPIO_INTR_DISABLE,
    };
    esp_err_t ret = gpio_config(&gas_pin_config);
    return ret;
}

void read_gas_sensor(uint8_t delay, uint8_t gas_pin){
    //prevent watchdog forceful stop in this task
    vTaskDelay(1);
    uint8_t gas_present;
    while(true){
        gas_present = gpio_get_level(gas_pin);

        //TODO
        //Send data to wifi host and (?)preserve it(?)

        vTaskDelay(delay);
    }
    
}
