# Создадим структуру Redux Toolkit store со слайсом и базовой конфигурацией
store_dir = os.path.join(frontend_src_path, "store")
slice_path = os.path.join(store_dir, "assemblySlice.ts")
index_path = os.path.join(store_dir, "index.ts")

# Код слайса
slice_code = """
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AssemblyState {
  currentAssemblyId: string | null;
}

const initialState: AssemblyState = {
  currentAssemblyId: null,
};

const assemblySlice = createSlice({
  name: 'assembly',
  initialState,
  reducers: {
    setAssemblyId(state, action: PayloadAction<string | null>) {
      state.currentAssemblyId = action.payload;
    },
  },
});

export const { setAssemblyId } = assemblySlice.actions;
export default assemblySlice.reducer;
"""