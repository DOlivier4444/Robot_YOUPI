
int max_array_int(int array[], int sizeOfArray) {

  int maxValue = abs(array[0]);

  for (int i = 1; i < sizeOfArray; i++) {  // store the maximum value of movements[] in max_value
    if ( abs(array[i]) > maxValue ) {
      maxValue = abs(array[i]);
    }
  }
  return maxValue;
}
