package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"sort"
)


func main() {
	// LOAD cape file
	capefile, err := os.Open("data/cape.txt")
	if err != nil {
		panic(err)
	}

	defer capefile.Close()
	CAPE_LST := []float64{}
	creader := bufio.NewReader(capefile)

	for {
		line, _, err := creader.ReadLine()

		if err == io.EOF {
			break
		}
		cape, _ := strconv.ParseFloat(string(line), 64)
		CAPE_LST = append(CAPE_LST, cape)
	}
	CAPE_LST = CAPE_LST[:756]
	// let's sort it for easy ranking
	sort.Float64s(CAPE_LST)
	b := len(CAPE_LST) / 2
	c := len(CAPE_LST) * 3 / 4
	d := len(CAPE_LST) * 8 / 10
	e := len(CAPE_LST) * 85 / 100
	f := len(CAPE_LST) * 9 / 10
	g := len(CAPE_LST) * 95 / 100
	fmt.Println(CAPE_LST[b], CAPE_LST[c], CAPE_LST[d], CAPE_LST[e], CAPE_LST[f], CAPE_LST[g])
}
