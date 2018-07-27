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


static int tx_count;


static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from){
  /* do nothing */
}
static void
broadcast_sent (struct broadcast_conn *ptr, int status, int num_tx){

	static char msg[] = "";

	switch (status){

		case MAC_TX_OK:
			tx_count++;
			process_post_synch(&sender_proc, PROCESS_EVENT_CONTINUE, msg);
			break;

		case MAC_TX_ERR:
		case MAC_TX_COLLISION:
			printf("sent callback: status %d\n", status);
			break;

		default:
			printf("sent callback: unhandled status %d \n", status);
			break;
	}
}

static const struct broadcast_callbacks recv_callbacks = {broadcast_recv, broadcast_sent};
static struct broadcast_conn broadcast;

PROCESS_THREAD(sender_proc, ev, data)
{
  static uint8_t payload[110];
  static int i;
  static clock_time_t begin_time, end_time;

	static int tx_payload_size;
	static int tx_delay;
	static int cca_thresh, input;
	static struct etimer et;

  PROCESS_EXITHANDLER(broadcast_close(&broadcast));
  PROCESS_BEGIN();

	broadcast_open(&broadcast, 125, &recv_callbacks);

  for (i = 0; i < 110; i++) payload[i] = (uint8_t) i;

	/* default settings */
	tx_payload_size = 110;

	printf("ready\n");

	// wait for serial "start"
	while(1){

		PROCESS_YIELD_UNTIL(ev == serial_line_event_message && strcmp((char*)data, "start")==0);

		PROCESS_YIELD_UNTIL(ev == serial_line_event_message);
		input = atoi((char*)data);

		tx_payload_size = input;
		tx_count = 0;

		begin_time = clock_time();

		for (i = 0; i < MAX_PKT_NUM; ++i) {

			packetbuf_copyfrom(payload, (uint16_t) tx_payload_size);
			broadcast_send(&broadcast);

			leds_toggle(LEDS_GREEN);
			PROCESS_WAIT_EVENT_UNTIL(ev == PROCESS_EVENT_CONTINUE);
		}

		end_time = clock_time();
		printf("finished\n");
		printf("%d\t%lu\n", tx_count, end_time-begin_time);
	}

  PROCESS_END();
}
