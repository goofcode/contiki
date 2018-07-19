
// #define TEST_CSMA
// #define TEST_DUTY_CYCLE
// #define TEST_NO_AUTO_ACK

#define MAX_PKT_NUM 1000
#define CHANNEL_NUM 125

// mac protocol
#undef NETSTACK_CONF_MAC
#ifdef TEST_CSMA
#define NETSTACK_CONF_MAC       csma_driver
#else
#define NETSTACK_CONF_MAC       nullmac_driver
#endif

// duty cycling
#ifdef TEST_DUTY_CYCLE
#undef NETSTACK_CONF_RDC_CHANNEL_CHECK_RATE
#define NETSTACK_CONF_RDC_CHANNEL_CHECK_RATE TEST_DC_CHECK_RATE
#else
#undef NETSTACK_CONF_RDC
#define NETSTACK_CONF_RDC nullrdc_driver
#endif

// auto ACK
#ifdef TEST_NO_AUTO_ACK
#undef CC2420_CONF_AUTOACK
#define CC2420_CONF_AUTOACK 0
#endif
