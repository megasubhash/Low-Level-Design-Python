# Rate Limiter System Design Requirements

## Functional Requirements

1. **Limit API requests**: The system should limit the number of requests a client can make within a specific time window.

2. **Multiple rate limiting algorithms**: Implement at least two different rate limiting algorithms:
   - Token Bucket
   - Sliding Window
   - Fixed Window Counter (optional)
   - Leaky Bucket (optional)

3. **Configurable limits**: Allow different limits for different clients/API endpoints.

4. **Response handling**: When a request is rate limited, return an appropriate error response with information about when the client can retry.

## Non-Functional Requirements

1. **Low latency**: The rate limiter should add minimal overhead to API requests (< 10ms).

2. **High availability**: The system should be highly available with no single point of failure.

3. **Scalability**: The solution should work in a distributed environment.

4. **Accuracy**: The rate limiter should be accurate in counting requests and enforcing limits.

## System Constraints

1. **Memory usage**: Optimize for memory efficiency, especially when handling millions of clients.

2. **Synchronization**: Consider race conditions in a distributed environment.

## Expected Deliverables

1. **Code implementation**: Implement the core rate limiting algorithms.

2. **API design**: Design a clean API for the rate limiter.

3. **Testing**: Include unit tests for your implementation.

4. **Documentation**: Document your design decisions and trade-offs.

## Discussion Points

1. How would you handle distributed rate limiting?
2. How would you handle different time windows (per second, minute, hour, day)?
3. What data structures would you use for efficient implementation?
4. How would you handle clock skew in a distributed environment?
5. How would your system scale to handle millions of clients?

## Evaluation Criteria

1. **Correctness**: Does the solution correctly implement rate limiting?
2. **Design**: Is the solution well-designed and maintainable?
3. **Performance**: Is the solution efficient in terms of time and space complexity?
4. **Scalability**: Can the solution scale to handle high loads?
5. **Code quality**: Is the code clean, well-structured, and well-tested?
