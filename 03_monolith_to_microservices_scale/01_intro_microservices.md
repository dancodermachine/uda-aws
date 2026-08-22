# Introduction to Microservices
## 1. Intro
| Monolith | Microservice |
|---|---|
| Utilize a powerful, more costly machine | Utilize smaller, cost-effective machines for what we need |
| Codebase is centralized and easy to manage | Flexibility to implement logic in a way that makes sense for the team and business |
| Code is easily shared across the project | Lean to target a specific business purpose |
| Scoped for worst-case usage across all parts of the application | Interfaces set up for building out other applications |
| — | Try not to overcommit and pay for resources that aren't needed |

## 2. When not to use Microservices
**Monoliths Are Not Bad!**

Microservices designs are another architectural pattern and are not intended to replace monolith applications. We should not blindly build applications as microservices without understanding the tradeoffs. Doing so could actually decrease productivity!

One way to think about this is to revisit our analogy with the Sports Superstore. Does it make sense for every aspiring small business owner to open and manage multiple stores at once?

Considerations for Not Using Microservices:
* **System Complexity**: Rather than deploying a single application, we would be deploying multiple modules separately. There is more overhead in setting up projects.
* **Network Latency**: By introducing a network between modules, we have increased latency in application performance and will find it harder to debug our application.
* **Difficulty with Debugging**: We can no longer rely on a stack trace or tools that can help us pinpoint where a bug is. We may end up relying on logging to find causes of issues.