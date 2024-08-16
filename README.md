# ZMQ - Examples

[Read More On. . .](https://zguide.zeromq.org/docs/chapter2/)

## Client-Server Patterns

1. **REQ and REP (Request and Reply)**

   - **REQ (Request)**: This socket sends a request and waits for a reply.
   - **REP (Reply)**: This socket waits for a request, processes it, and sends back a reply.
   - **Use Case**: Simple client-server communication. The client sends a request, and the server sends a reply.

2. **REQ and ROUTER**

   - **REQ (Request)**: Same as above, but it inserts an extra null frame.
   - **ROUTER**: This socket can route messages to specific REQ sockets based on their identity.
   - **Use Case**: Advanced request-reply communication with message routing capabilities.

3. **DEALER and REP**

   - **DEALER**: This socket is like an asynchronous REQ, sending multiple requests without waiting for replies.
   - **REP (Reply)**: Same as above, but it assumes a null frame.
   - **Use Case**: More flexible client-server communication where the client can send multiple requests.

4. **DEALER and ROUTER**

   - **DEALER**: Same as above.
   - **ROUTER**: Same as above.
   - **Use Case**: Advanced and flexible request-reply communication with complex routing and asynchronous message handling.

5. **DEALER and DEALER**

   - **DEALER**: Both sockets can send and receive messages asynchronously.
   - **Use Case**: Peer-to-peer communication where both sides can send and receive messages freely.

6. **ROUTER and ROUTER**
   - **ROUTER**: Both sockets can route messages to specific sockets based on their identity.
   - **Use Case**: Complex routing scenarios where multiple endpoints need to communicate with each other flexibly.

## Publish-Subscribe Pattern

1. **PUB and SUB (Publisher and Subscriber)**
   - **PUB (Publisher)**: This socket sends messages to all connected subscribers.
   - **SUB (Subscriber)**: This socket receives messages from the publisher. Subscribers can filter messages based on topics.
   - **Use Case**: Broadcasting messages from one sender to multiple receivers, useful for scenarios like news updates or event notifications.

## Push-Pull Pattern

1. **PUSH and PULL**
   - **PUSH**: This socket sends messages to connected PULL sockets.
   - **PULL**: This socket receives messages from PUSH sockets.
   - **Use Case**: Task distribution, where tasks are pushed to workers for parallel processing.

## Exclusive Pair Pattern

1. **PAIR and PAIR**
   - **PAIR**: This socket connects exclusively to one other PAIR socket.
   - **Use Case**: Simple one-to-one communication, useful for scenarios like inter-thread communication within a single application.

## Summary in Client-Server Terms:

- **Client-Server (REQ-REP)**: One client sends a request, and one server replies.
- **Advanced Client-Server (REQ-ROUTER)**: Clients send requests to a router that forwards them to the correct server.
- **Asynchronous Client-Server (DEALER-REP)**: Clients send multiple requests without waiting for replies.
- **Flexible Client-Server (DEALER-ROUTER)**: Advanced routing and asynchronous communication.
- **Peer-to-Peer (DEALER-DEALER)**: Both parties send and receive messages freely.
- **Complex Routing (ROUTER-ROUTER)**: Multiple endpoints communicate with routing.

## Summary in Publisher-Subscriber Terms:

- **Broadcasting (PUB-SUB)**: One sender sends messages to many receivers.

## Summary in Push-Pull Terms:

- **Task Distribution (PUSH-PULL)**: Tasks are pushed to workers for processing.

## Summary in Pair Terms:

- **Exclusive Communication (PAIR-PAIR)**: One-to-one communication, typically used within the same application for inter-thread communication.
