//#define TEST_DUTY_CYCLE
//#define TEST_NO_AUTO_ACK

//#undef NETSTACK_CONF_MAC
//#define NETSTACK_CONF_MAC       nullmac_driver


// duty cycling
#ifdef TEST_DUTY_CYCLE
#undef NETSTACK_CONF_RDC_CHANNEL_CHECK_RATE
#define NETSTACK_CONF_RDC_CHANNEL_CHECK_RATE TEST_DC_CHECK_RATE
#else
#undef NETSTACK_CONF_RDC
#define NETSTACK_CONF_RDC nullrdc_driver
#endif
