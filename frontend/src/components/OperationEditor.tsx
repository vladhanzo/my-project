// frontend/src/components/OperationEditor.tsx
import { useForm, useFieldArray, Controller } from 'react-hook-form'
import { Box, Button, Grid, IconButton, MenuItem, TextField, Typography } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'

type Action = {
  name: string
  value: number
  unit: string
}

type FormData = {
  actions: Action[]
}

const unitOptions = ['mm', 'cm', 'm']

function previewComponents(data: FormData) {
  console.log(data)
}

export default function OperationEditor() {
  const { control, handleSubmit, watch, formState: { errors } } = useForm<FormData>({
    defaultValues: {
      actions: [{ name: '', value: 0, unit: '' }]
    }
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'actions'
  })

  const onSubmit = (data: FormData) => {
    previewComponents(data)
  }

  const actions = watch('actions')

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Typography variant="h6" mb={2}>Operation Editor</Typography>
      {fields.map((field, index) => (
        <Grid container spacing={2} key={field.id} alignItems="center">
          <Grid item xs={4}>
            <Controller
              name={`actions.${index}.name`}
              control={control}
              rules={{ required: true }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Name"
                  error={!!errors.actions?.[index]?.name}
                />
              )}
            />
          </Grid>
          <Grid item xs={3}>
            <Controller
              name={`actions.${index}.value`}
              control={control}
              rules={{
                required: true,
                min: 0,
                validate: (value) => !isNaN(Number(value))
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  type="number"
                  fullWidth
                  label="Value"
                  error={!!errors.actions?.[index]?.value}
                />
              )}
            />
          </Grid>
          <Grid item xs={3}>
            <Controller
              name={`actions.${index}.unit`}
              control={control}
              rules={{
                required: true,
                validate: (unit) => unitOptions.includes(unit)
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  fullWidth
                  label="Unit"
                  error={!!errors.actions?.[index]?.unit}
                >
                  {unitOptions.map((option) => (
                    <MenuItem key={option} value={option}>{option}</MenuItem>
                  ))}
                </TextField>
              )}
            />
          </Grid>
          <Grid item xs={2}>
            <IconButton onClick={() => remove(index)}>
              <Delete />
            </IconButton>
          </Grid>
        </Grid>
      ))}
      <Box mt={2}>
        <Button variant="outlined" startIcon={<Add />} onClick={() => append({ name: '', value: 0, unit: '' })}>
          Add Action
        </Button>
      </Box>
      <Box mt={2}>
        <Button variant="contained" type="submit">
          Preview
        </Button>
      </Box>
    </Box>
  )
}
