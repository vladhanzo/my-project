// frontend/src/components/ComponentSelector.tsx
import { Autocomplete, CircularProgress, TextField } from '@mui/material'
import { useEffect, useMemo, useState } from 'react'
import { debounce } from 'lodash'
import axios from 'axios'

type ComponentOption = {
  id: string
  label: string
}

type ComponentSelectorProps = {
  value: ComponentOption[]
  onChange: (value: ComponentOption[]) => void
}

export default function ComponentSelector({ value, onChange }: ComponentSelectorProps) {
  const [inputValue, setInputValue] = useState('')
  const [options, setOptions] = useState<ComponentOption[]>([])
  const [loading, setLoading] = useState(false)

  const fetchComponents = async (query: string) => {
    setLoading(true)
    try {
      const response = await axios.get('/api/components/search', {
        params: { q: query }
      })
      setOptions(response.data)
    } finally {
      setLoading(false)
    }
  }

  const debouncedFetch = useMemo(
    () =>
      debounce((query: string) => {
        if (query.length >= 3) fetchComponents(query)
      }, 500),
    []
  )

  useEffect(() => {
    debouncedFetch(inputValue)
  }, [inputValue, debouncedFetch])

  return (
    <Autocomplete
      multiple
      filterSelectedOptions
      options={options}
      getOptionLabel={(option) => option.label}
      value={value}
      onChange={(_, newValue) => onChange(newValue)}
      inputValue={inputValue}
      onInputChange={(_, newInputValue) => setInputValue(newInputValue)}
      loading={loading}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Select Components"
          variant="outlined"
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <>
                {loading ? <CircularProgress color="inherit" size={20} /> : null}
                {params.InputProps.endAdornment}
              </>
            )
          }}
        />
      )}
    />
  )
}
