#include "contiki.h"
#include "net/rime/rime.h"

#include <stdio.h> /* For printf() */

#define CHANNEL_NUM 255

#define EXPECTED_TX_DURATION 30


/*---------------------------------------------------------------------------*/
PROCESS(project_1_receiver, "receiver process");
AUTOSTART_PROCESSES(&project_1_receiver);
/*---------------------------------------------------------------------------*/

static int count = 0;
static clock_time_t begin_time, end_time;

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  // if this is first packet
  if (count == 0)
    begin_time = clock_time();

  end_time = clock_time();

  count++;
  printf("message received from %d.%d: '%s'\n",
         from->u8[0], from->u8[1], (char *)packetbuf_dataptr());
}
static const struct broadcast_callbacks recv_callbacks = {broadcast_recv};
static struct broadcast_conn broadcast;

PROCESS_THREAD(project_1_receiver, ev, data)
{
  static struct etimer et;

  PROCESS_EXITHANDLER(broadcast_close(&broadcast);)
  PROCESS_BEGIN();

  broadcast_open(&broadcast, CHANNEL_NUM, &recv_callbacks);

  etimer_set(&et, EXPECTED_TX_DURATION * CLOCK_SECOND);
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

  printf("%d packets received in %lu (CLOCK_SECOND: %lu) \n", 
    count, end_time-begin_time, CLOCK_SECOND);

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
