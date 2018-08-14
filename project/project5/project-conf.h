//#define TEST_DUTY_CYCLE

#undef NETSTACK_CONF_MAC
#define NETSTACK_CONF_MAC       csma_driver
//#define NETSTACK_CONF_MAC 				nullmac_driver

#undef NETSTACK_CONF_RDC
#define NETSTACK_CONF_RDC nullrdc_driver
