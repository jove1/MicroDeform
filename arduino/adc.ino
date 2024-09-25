#include <SPI.h>

#define FREQ      20000 // 20kHz
#define DECODE        1 // unpack 18bit values?

#define PIN_CNVST     9 // must have pwm (arduino)
#define PIN_CS       10 // BOARD_SPI_SS[0-3]
#define PIN_BUSY     11 // any digital


#if DECODE
  #define BUFFER_TYPE int32_t
  #define BUFFER_SIZE 8192 // 0.1s @ 20kHz
#else
  #define BUFFER_TYPE uint8_t
  #define BUFFER_SIZE 18000
#endif


BUFFER_TYPE buffer1[BUFFER_SIZE];
BUFFER_TYPE buffer2[BUFFER_SIZE];
BUFFER_TYPE *acq_buffer;
BUFFER_TYPE *send_buffer;
volatile bool data_to_send;
int pos;

void setup() {
  // double buffer
  pos = 0;
  data_to_send = false;
  acq_buffer = buffer1;
  send_buffer = buffer2;
  
  // USB
  SerialUSB.begin(0); 

  // SPI
  SPI.begin(PIN_CS);
  SPI.setBitOrder(PIN_CS, MSBFIRST);
  SPI.setClockDivider(PIN_CS, 4);     // max. 22.5MHz
  SPI.setDataMode(PIN_CS, SPI_MODE2); // CPOL=1 CPHA=0
  
  // ~BUSY interrupt
  pinMode(PIN_BUSY, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIN_BUSY), adc_read, FALLING);

  // PWM CNVST
  const PinDescription *p = &g_APinDescription[PIN_CNVST];
  pmc_enable_periph_clk(PWM_INTERFACE_ID);
  PIO_Configure(p->pPort, p->ulPinType, p->ulPin, p->ulPinConfiguration);
  PWMC_ConfigureChannel(PWM_INTERFACE, p->ulPWMChannel, PWM_CMR_CPRE_MCK, 0, PWM_CMR_CPOL);
  PWMC_SetPeriod(PWM_INTERFACE, p->ulPWMChannel, VARIANT_MCK/FREQ);
  PWMC_SetDutyCycle(PWM_INTERFACE, p->ulPWMChannel, VARIANT_MCK/10000000); // 100ns
  PWMC_EnableChannel(PWM_INTERFACE, p->ulPWMChannel);
}


#define decode18bit(P, Q) \
  (Q)[0] = ( (P[0] << 24) | (P[1] << 16) | (P[2] <<  8) ) >> 14; \
  (Q)[1] = ( (P[2] << 26) | (P[3] << 18) | (P[4] << 10) ) >> 14; \
  (Q)[2] = ( (P[4] << 28) | (P[5] << 20) | (P[6] << 12) ) >> 14; \
  (Q)[3] = ( (P[6] << 30) | (P[7] << 22) | (P[8] << 14) ) >> 14;

void adc_read() {
#if DECODE
  uint8_t P[9];
  //P[0] = P[1] = P[2] = P[3] = P[4] = P[5] = P[6] = P[7] = P[8] = 0xff;
  SPI.transfer(PIN_CS, P, 9);
  decode18bit(P, acq_buffer+pos)
  pos += 4;
#else
  SPI.transfer(PIN_CS, acq_buffer+pos, 9);
  pos += 9;
#endif

  if (pos >= BUFFER_SIZE) {
    pos = 0;
    
    // swap buffers
    BUFFER_TYPE *tmp = acq_buffer;
    acq_buffer = send_buffer;
    send_buffer = tmp;

    data_to_send = true;
  }

}


void loop() {
  if (data_to_send) {
    SerialUSB.write((uint8_t*)send_buffer, BUFFER_SIZE*sizeof(BUFFER_TYPE));
    data_to_send = false;
  }
}
