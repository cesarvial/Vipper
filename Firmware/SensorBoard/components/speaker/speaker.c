#include <stdio.h>
#include "driver/i2s.h"
#include "driver/adc.h"
#include "speaker.h"

#define SAMPLE_RATE 16000
#define SAMPLE_BITS 16

/**
 * @brief I2S ADC mode init
 * 
 */
void speaker_init(void){
    // int i2s_num = EXAMPLE_I2S_NUM;
    // i2s_config_t i2s_config = {
    //     .mode = I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_TX | I2S_MODE_DAC_BUILT_IN | I2S_MODE_ADC_BUILT_IN,
    //     .sample_rate = SAMPLE_RATE,
    //     .bits_per_sample = SAMPLE_BITS,
    //     .communication_format = I2S_COMM_FORMAT_STAND_MSB,
    //     .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
    //     .intr_alloc_flags = 0,
    //     .dma_buf_count = 2,
    //     .dma_buf_len = 1024,
    //     .use_apll = 1,
    // };
    // //install and start i2s driver
    //  i2s_driver_install(i2s_num, &i2s_config, 0, NULL);
    //  //init DAC pad
    //  i2s_set_dac_mode(I2S_DAC_CHANNEL_BOTH_EN);
    //  //init ADC pad
    //  i2s_set_adc_mode(I2S_ADC_UNIT, I2S_ADC_CHANNEL);
}

// /**
//  * @brief Set i2s clock for example audio file
//  */
// void example_set_file_play_mode(void)
// {
//     i2s_set_clk(EXAMPLE_I2S_NUM, 16000, EXAMPLE_I2S_SAMPLE_BITS, 1);
// }

// void play_message(){
//     //4. Play an example audio file(file format: 8bit/16khz/single channel)
//         printf("Playing file example: \n");
//         int offset = 0;
//         int tot_size = sizeof(audio_table);
//         example_set_file_play_mode();
//         while (offset < tot_size) {
//             int play_len = ((tot_size - offset) > (4 * 1024)) ? (4 * 1024) : (tot_size - offset);
//             int i2s_wr_len = example_i2s_dac_data_scale(i2s_write_buff, (uint8_t*)(audio_table + offset), play_len);
//             i2s_write(EXAMPLE_I2S_NUM, i2s_write_buff, i2s_wr_len, &bytes_written, portMAX_DELAY);
//             offset += play_len;
//             example_disp_buf((uint8_t*) i2s_write_buff, 32);
//         }
//         vTaskDelay(100 / portTICK_PERIOD_MS);
//         example_reset_play_mode();
// }