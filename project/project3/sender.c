#include "contiki.h"
#include "net/rime/rime.h"
#include "dev/leds.h"
#include "contiki-net.h"
#include "dev/serial-line.h"

#include <stdio.h> /* For printf() */
#include <stdlib.h>

#define MAX_PKT_NUM 1000

/*---------------------------------------------------------------------------*/
PROCESS(sender_proc, "sender process");
AUTOSTART_PROCESSES(&sender_proc);
/*---------------------------------------------------------------------------*/


int tx_count;

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  /* do nothing */
}
static const struct broadcast_callbacks recv_callbacks = {broadcast_recv};
static struct broadcast_conn broadcast;

PROCESS_THREAD(sender_proc, ev, data)
{
  static uint8_t payload[110];
  static int i;
  static clock_time_t begin_time, end_time;

	static int tx_payload_size;
	static int tx_delay;
	static int result, txpower;
	static int cca_thresh, input;
	static struct etimer et;

  PROCESS_EXITHANDLER(broadcast_close(&broadcast));
  PROCESS_BEGIN();

  for (i = 0; i < 110; i++) payload[i] = (uint8_t) i;
  broadcast_open(&broadcast, 125, &recv_callbacks);

	tx_payload_size = 110;
	tx_delay = 2;
	cca_thresh = -90;

	printf("ready\n");

	// wait for serial "start"
	while(1){

		PROCESS_YIELD_UNTIL(ev == serial_line_event_message && strcmp((char*)data, "start")==0);

		PROCESS_YIELD_UNTIL(ev == serial_line_event_message);
		input = atoi((char*)data);

//		NETSTACK_RADIO.set_value(RADIO_PARAM_CCA_THRESHOLD, input);
//		NETSTACK_RADIO.get_value(RADIO_PARAM_CCA_THRESHOLD, &input);
//		printf("cca threshold: %d\n", input);

//		tx_delay = input;

		tx_payload_size = input;
		tx_count = 0;

		begin_time = clock_time();

		for (i = 0; i < MAX_PKT_NUM; ++i) {

				// pausing process might be needed here,
			// because this process could monopolize CPU time
//			PROCESS_PAUSE();

			packetbuf_copyfrom(payload, (uint16_t) tx_payload_size);
			result = broadcast_send(&broadcast);

			leds_toggle(LEDS_GREEN);

			etimer_set(&et, tx_delay);
			PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
		}

		end_time = clock_time();
		printf("finished\n");
		printf("%d\t%lu\n", tx_count, end_time-begin_time);
	}

  PROCESS_END();
}
