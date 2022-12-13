import asyncio
import aiofiles


def res_giver():
    return ((i, i * i) for i in range(10000))


async def file_write(i: int) -> None:
    res = res_giver()
    print(f'File {i} writing')
    async with aiofiles.open(f'async_{i}.csv', 'w', encoding='utf-8') as csvfile:
        # writer = csv.writer(csvfile, delimiter=',',quoting= csv.QUOTE_NONE, quotechar='"')
        # writer.writerows([(i, '\t', i*i) for i in range(1000000)])
        await csvfile.writelines((',\t'.join((str(r[0]), str(r[1]), '\n')) for r in res))
    print(f'File {i} ended')


async def main():
    await asyncio.gather(*(file_write(j) for j in range(4)))


if __name__ == '__main__':
    asyncio.run(main())
