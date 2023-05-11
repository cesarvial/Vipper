#ifndef __GAS_SENSOR_H__
#define __GAS_SENSOR_H__

#include "esp_err.h"

esp_err_t gas_sensor_init(uint8_t gas_pin);
void read_gas_sensor(uint8_t delay, uint8_t gas_pin);

#endif //__GAS_SENSOR_H__