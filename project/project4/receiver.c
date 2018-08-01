#include "contiki.h"
#include "net/rime/rime.h"
#include "dev/leds.h"
#include "dev/serial-line.h"
#include "contiki-net.h"

#include <stdio.h> /* For printf() */

/*---------------------------------------------------------------------------*/
PROCESS(receiver_proc, "receiver process");
AUTOSTART_PROCESSES(&receiver_proc);
/*---------------------------------------------------------------------------*/

static int rx_count;
static int receiving = -1;
static clock_time_t begin_time, end_time;

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  if(receiving == 1){
    // if this is first packet
    if (rx_count == 0)
      begin_time = clock_time();

    end_time = clock_time();

		rx_count++;
    leds_toggle(LEDS_BLUE);
  }
  else{
    leds_toggle(LEDS_ALL);
  }
}

static const struct broadcast_callbacks recv_callbacks = {broadcast_recv};
static struct broadcast_conn broadcast;

PROCESS_THREAD(receiver_proc, ev, data)
{
  PROCESS_EXITHANDLER(broadcast_close(&broadcast);)
  PROCESS_BEGIN();

  broadcast_open(&broadcast, 125, &recv_callbacks);
  printf("ready\n");

  while(1){

		// wait for serial "start"
		PROCESS_WAIT_EVENT_UNTIL(ev == serial_line_event_message && strcmp((char*)data, "start") == 0);

		rx_count = 0;
		receiving = 1;

    // wait for serial "stop"
		PROCESS_WAIT_EVENT_UNTIL(ev == serial_line_event_message && strcmp((char*)data, "stop") == 0);
		receiving = -1;


    printf("%d\t%lu\n", rx_count, end_time-begin_time);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
