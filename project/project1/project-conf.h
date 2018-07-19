
#define NULL_TEST

#ifdef NULL_TEST

    #define NETSTACK_CONF_RDC       nullrdc_driver
    #define NETSTACK_CONF_MAC       nullmac_driver
    #define NETSTACK_CONF_FRAMER    framer_nullmac

#else

    #define NETSTACK_CONF_RDC       nullrdc_driver
    #define NETSTACK_CONF_MAC       csma_driver
#endif

