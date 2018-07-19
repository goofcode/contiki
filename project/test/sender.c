#include "contiki.h"
#include "net/rime/rime.h"
#include "dev/leds.h"
#include "contiki-net.h"
#include "dev/serial-line.h"
#include "project-conf.h"

#include <stdio.h> /* For printf() */


/*---------------------------------------------------------------------------*/
PROCESS(sender_proc, "sender process");
AUTOSTART_PROCESSES(&sender_proc);
/*---------------------------------------------------------------------------*/

static int tx_payload_size;

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
  static int count = 0, i;
  static struct etimer et;
  static clock_time_t begin_time, end_time;


  PROCESS_EXITHANDLER(broadcast_close(&broadcast));
  PROCESS_BEGIN();

  for (i = 0; i < 110; i++)
    payload[i] = i;

  printf("ready\n");

  broadcast_open(&broadcast, 125, &recv_callbacks);

  while(1){
    // wait for serial "start"
    while(1){

      PROCESS_YIELD_UNTIL(ev == serial_line_event_message && strcmp((char*)data, "send\n"));

      packetbuf_copyfrom(payload, tx_payload_size);
      broadcast_send(&broadcast);
      leds_toggle(LEDS_GREEN);
    }
  }
  PROCESS_END();
}
