
int Maximum_Value_Of_Int_Array(int Array[], int SizeOfArray) {

  int max_value = abs(Array[0]);

  for (int i = 1; i < SizeOfArray; i++) {  // store the maximum value of movements[] in max_value
    if ( abs(Array[i]) > max_value ) {
      max_value = abs(Array[i]);
    }
  }
  return max_value;
}
