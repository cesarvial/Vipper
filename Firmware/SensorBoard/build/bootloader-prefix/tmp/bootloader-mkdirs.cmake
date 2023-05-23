# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/hexdev04/esp/esp-idf/components/bootloader/subproject"
  "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader"
  "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix"
  "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix/tmp"
  "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix/src/bootloader-stamp"
  "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix/src"
  "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/hexdev04/Documents/Projetos/vipper/Vipper/Firmware/SensorBoard/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
