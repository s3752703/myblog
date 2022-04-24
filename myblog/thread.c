#include <pthread.h>

#include <stdio.h>

#include <sys/time.h>

#include <time.h>

#include <stdlib.h>

#include <sys/types.h>

#include <unistd.h>

#include <string.h>



#define NUM_THREADS 20



int perload = 10;

struct timeval t1, t2;

double elapsedTime;



void *printHello(void *threadid)

{

  long tid;

  tid = (long)threadid;

  int i;

  int sum;

	

  for (i = 1; i <= perload; i++){

		

		int j;

    for(j=0; j <= 100000000; j++){

      sum = sum + 1;

		}

		//sum = sum + 1;

		//sleep(1);		



	}

	

	// compute and print the elapsed time in millisec

	gettimeofday(&t2, NULL);

  elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;   // sec to ms

  elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;  // us to ms

  printf("time = %.2f, thread #%ld!\n",elapsedTime,tid);

   

  pthread_exit(NULL);

  //exit(EXIT_SUCCESS);

 }



 int main (int argc, char *argv[])

 {

  gettimeofday(&t1, NULL);

	

  pthread_t threads[NUM_THREADS];

  int rc;

  long t;

   

  for(t=0; t<NUM_THREADS; t++){

    printf("In main: creating thread %ld\n", t);

    rc = pthread_create(&threads[t], NULL, printHello, (void *)t);

     

    if (rc){

     printf("ERROR; return code from pthread_create() is %d\n", rc);

      printf("Error is %s\n", strerror(rc));

     exit(EXIT_FAILURE);

    }

  }



  // Last thing that main() should do

  pthread_exit(NULL);

  //exit(0); 

}