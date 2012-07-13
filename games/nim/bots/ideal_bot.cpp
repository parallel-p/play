#include <cstdio>

const int MAX_COUNT = (int)1e5;
int heap_sizes[MAX_COUNT];

int main()
{
    while (1)
    {
        int heaps_count = 0;
        while (scanf("%d", &heap_sizes[heaps_count]) == 1)
        {
            ++heaps_count;
        }

        int global_xor = 0;
        for (int i = 0; i < heaps_count; ++i)
        {
            global_xor ^= heap_sizes[i];
        }

        if (global_xor)
        {
            for (int i = 0; i < heaps_count; ++i)
            {
                int new_size = global_xor ^ heap_sizes[i];
                if (heap_sizes[i] >= new_size)
                {
                    printf("%d %d\n", i, heap_sizes[i] - new_size);
                    break;
                }
            }
        }
        else
        {
            for (int i = 0; i < heaps_count; ++i)
            {
                if (heap_sizes[i])
                {
                    printf("%d %d\n", i, 1);
                    break;
                }
            }
        }

        fflush(stdout);
    }
    return 0;
}
