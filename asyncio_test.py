import asyncio
import time

# 1️⃣ Basic async function (simulates network request)
async def async_task(name, delay):
    print(f"{name} started...")
    await asyncio.sleep(delay)  # Yields execution
    print(f"{name} finished after {delay} seconds")
    return name

# 2️⃣ Running tasks sequentially vs concurrently
async def test_sequential_vs_concurrent():
    print("\n=== Running Sequentially ===")
    start = time.time()
    await async_task("Task 1", 2)  # Runs first
    await async_task("Task 2", 3)  # Runs after Task 1 completes
    print(f"Sequential execution took {time.time() - start:.2f} seconds")

    print("\n=== Running Concurrently ===")
    start = time.time()
    await asyncio.gather(  # Runs all tasks concurrently
        async_task("Task 1", 2),
        async_task("Task 2", 3)
    )
    print(f"Concurrent execution took {time.time() - start:.2f} seconds")

# 3️⃣ Handling a blocking function using run_in_executor()
def blocking_function():
    print("Blocking function started...")
    time.sleep(3)  # Simulates a long-running computation
    print("Blocking function finished")

async def test_run_in_executor():
    print("\n=== Running Blocking Function in Executor ===")
    loop = asyncio.get_running_loop()
    start = time.time()
    await loop.run_in_executor(None, blocking_function)  # Runs in a separate thread
    print(f"Executor finished in {time.time() - start:.2f} seconds")

# 4️⃣ CPU-bound task to show that asyncio doesn't provide true parallelism
def cpu_heavy_task(n):
    print(f"CPU-heavy task {n} started...")
    total = sum(i * i for i in range(10**6))  # Heavy computation
    print(f"CPU-heavy task {n} finished")
    return total

async def test_cpu_bound():
    print("\n=== Running CPU-Bound Tasks in Asyncio (Will Not Be Parallel) ===")
    start = time.time()
    loop = asyncio.get_running_loop()
    # Runs CPU-bound functions in threads (since asyncio itself won't speed them up)
    result = await asyncio.gather(
        loop.run_in_executor(None, cpu_heavy_task, 1),
        loop.run_in_executor(None, cpu_heavy_task, 2),
    )
    print(f"CPU-bound tasks finished in {time.time() - start:.2f} seconds")

# 5️⃣ Main function to run all tests
async def main():
    await test_sequential_vs_concurrent()
    await test_run_in_executor()
    await test_cpu_bound()

# Run the asyncio event loop
asyncio.run(main())
