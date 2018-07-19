#include "contiki.h"
#include "net/rime/rime.h"
#include "dev/leds.h"
#include "dev/serial-line.h"

#include <stdio.h> /* For printf() */

/*---------------------------------------------------------------------------*/
PROCESS(receiver_proc, "receiver process");
AUTOSTART_PROCESSES(&receiver_proc);
/*---------------------------------------------------------------------------*/

static int count = 0;
static int receiving = -1;
static clock_time_t begin_time, end_time;

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  if(receiving){
    // if this is first packet
    if (count == 0)
      begin_time = clock_time();

    end_time = clock_time();

    count++;
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
  static struct etimer et;

  PROCESS_EXITHANDLER(broadcast_close(&broadcast);)
  PROCESS_BEGIN();

  broadcast_open(&broadcast, 125, &recv_callbacks);

  printf("ready\n");

  while(1){
    // wait for serial "start"
    while (1)
    {
      PROCESS_YIELD_UNTIL(
        ev == serial_line_event_message 
        && strcmp((char *)data, "start\n"));

      count = 0;
      receiving = 1;
      printf("start receiving\n");
      break;
    }

    // wait for serial "stop"
    while(1){
      PROCESS_YIELD_UNTIL(
          ev == serial_line_event_message 
          && strcmp((char *)data, "stop\n"));
     
      receiving = -1;
      printf("stop receiving\n");
      break;
    }
    
    printf("%d\t%lu\n", count, end_time-begin_time);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
