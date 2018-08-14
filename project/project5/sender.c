#include "contiki.h"
#include "net/rime/rime.h"
#include "dev/leds.h"
#include "contiki-net.h"
#include "dev/serial-line.h"

#include <stdio.h> /* For printf() */
#include <stdlib.h>
#include <net/linkaddr.h>
#include <sys/node-id.h>

#define MAX_PKT_NUM 1000

/*---------------------------------------------------------------------------*/
PROCESS(sender_proc, "sender process");
AUTOSTART_PROCESSES(&sender_proc);
/*---------------------------------------------------------------------------*/


static int tx_count;

static void
unicast_recv(struct unicast_conn *c, const linkaddr_t *from){
  /* do nothing */
}

static void
unicast_sent (struct unicast_conn *ptr, int status, int num_tx){

	if (status == MAC_TX_OK)
		tx_count++;
//	else
//		printf("broadcast sent: %d\n",status);

	// start next tx
	process_post(&sender_proc, PROCESS_EVENT_CONTINUE, "");
}

static const struct unicast_callbacks uc_callbacks = {unicast_recv, unicast_sent};
static struct unicast_conn uc;

PROCESS_THREAD(sender_proc, ev, data)
{
  static uint8_t payload[110];
  static clock_time_t begin_time, end_time;
	static int i, tx_payload_size, input;
	static linkaddr_t receiver_addr;

  PROCESS_EXITHANDLER(unicast_close(&uc));
  PROCESS_BEGIN();

  for (i = 0; i < 110; i++)
		payload[i] = (uint8_t) i;
	tx_payload_size = 110;

	unicast_open(&uc, 125, &uc_callbacks);

	printf("ready\n");

	// get receiver's addr
	PROCESS_WAIT_EVENT_UNTIL(ev==serial_line_event_message);
	receiver_addr.u16 = (uint16_t) atoi((char*) data);

	while(1){

		// wait for serial "start"
		PROCESS_WAIT_EVENT_UNTIL(ev == serial_line_event_message && strcmp((char*)data, "start")==0);

		PROCESS_WAIT_EVENT_UNTIL(ev == serial_line_event_message);
		input = atoi((char*)data);
		tx_payload_size = input;

		tx_count = 0;
		begin_time = clock_time();

		for (i = 0; i < MAX_PKT_NUM; ++i) {

			packetbuf_copyfrom(payload, (uint16_t) tx_payload_size);
			unicast_send(&uc, &receiver_addr);

			leds_toggle(LEDS_GREEN);
			PROCESS_WAIT_EVENT_UNTIL(ev==PROCESS_EVENT_CONTINUE);
		}

		end_time = clock_time();
		printf("finished\n");
		printf("%d\t%lu\n", tx_count, end_time-begin_time);
	}

  PROCESS_END();
}
