package Checksum

import (
	"errors"
)

func CheckSum(count int, input []int) (int, error) {
	var output int
	if count == 2 {
		for _, i := range input {
			for _, j := range input {
				if i+j == 2020 {
					return i * j, nil
				}
			}
		}
	}
	if count == 3 {
		for _, i := range input {
			for _, j := range input {
				for _, k := range input {
					if i+j+k == 2020 {
						return i * j * k, nil
					}
				}
			}
		}
	}

	return output, errors.New("Broken")
}
