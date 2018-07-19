#include "contiki.h"
#include "net/rime/rime.h"

#include <stdio.h> /* For printf() */

#define MAX_PKT_NUM 1000
#define PKT_SIZE 120
#define CHANNEL_NUM 255

#define WAIT_RX_DELAY 5

/*---------------------------------------------------------------------------*/
PROCESS(project_1_sender, "sender process");
AUTOSTART_PROCESSES(&project_1_sender);
/*---------------------------------------------------------------------------*/

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  /* do nothing */
}
static const struct broadcast_callbacks recv_callbacks = {broadcast_recv};
static struct broadcast_conn broadcast;

PROCESS_THREAD(project_1_sender, ev, data)
{
  static char payload[PKT_SIZE] = {0,};
  static int count = 0, i;
  static struct etimer et;
  static clock_time_t begin_time, end_time;

  PROCESS_EXITHANDLER(broadcast_close(&broadcast));
  PROCESS_BEGIN();

  for(i=0; i<PKT_SIZE-1; i++)
    payload[i] = 'a' + i;

  printf("Wait for receiver to start\n");
  etimer_set(&et, WAIT_RX_DELAY * CLOCK_SECOND);
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

  printf("Start transmitting\n");

  broadcast_open(&broadcast, CHANNEL_NUM, &recv_callbacks);

  begin_time = clock_time();

  while (count < MAX_PKT_NUM){

    packetbuf_copyfrom(payload, PKT_SIZE);

    broadcast_send(&broadcast);

    count++;

    PROCESS_PAUSE();
  }

  end_time = clock_time();

  printf("%d packets (%d bytes each) sent in %lu clocks (CLOCK_SECOND: %lu)\n", 
    count, PKT_SIZE, end_time-begin_time, CLOCK_SECOND);

  PROCESS_END();
}
