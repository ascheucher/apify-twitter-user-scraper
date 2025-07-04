# Usage and resources

**Learn about your Actors' memory and processing power requirements, their relationship with Docker resources, minimum requirements for different use cases and its impact on the cost.**

## Resources

[Actors](/platform/actors) run in [Docker containers](https://www.docker.com/resources/what-container/), which have a [limited amount of resources](https://phoenixnap.com/kb/docker-memory-and-cpu-limit) (memory, CPU, disk size, etc). When starting, the Actor needs to be allocated a certain share of those resources, such as CPU capacity that is necessary for the Actor to run.

![Setting an Actor's memory](/assets/images/memory-settings-6bb15c0d4061ce772fb90e677fa29b04.png)

Assigning an Actor a specific **Memory** capacity, also determines the allocated CPU power and its disk size.

Check out the [Limits](/platform/limits) page for detailed information on Actor memory, CPU limits, disk size and other limits.

### Memory

When invoking an Actor, the caller must specify the memory allocation for the Actor run. The memory allocation must follow these requirements:

- It must be a power of 2.
- The minimum allowed value is `128MB`
- The maximum allowed value is `32768MB`
- Acceptable values include: `128MB`, `256MB`, `512MB`, `1024MB`, `2048MB`, `4096MB`, `8192MB`, `16384MB`, and `32768MB`

Additionally, each user has a certain total limit of memory for running Actors. The sum of memory allocated for all running Actors and builds needs to be within this limit, otherwise the user cannot start a new Actor.

### CPU

The CPU allocation for an Actor is automatically computed based on the assigned memory, following these rules:

- For every `4096MB` of memory, the Actor receives one full CPU core
- If the memory allocation is not a multiple of `4096MB`, the CPU core allocation is calculated proportionally
- Examples:
    - `512MB` = 1/8 of a CPU core
    - `1024MB` = 1