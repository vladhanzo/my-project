// frontend/src/components/AssemblyDashboard.tsx
import { useEffect } from "react"
import { useAppDispatch, useAppSelector } from "@/hooks/useRedux"
import { fetchAssemblies, selectAssemblies } from "@/store/assemblySlice"
import {
  Table, TableHead, TableBody, TableRow, TableCell, TablePagination, TableSortLabel,
  TextField, MenuItem, Select, InputLabel, FormControl, Box, Grid
} from "@mui/material"
import { DatePicker } from "@mui/x-date-pickers"
import dayjs, { Dayjs } from "dayjs"

export default function AssemblyDashboard() {
  const dispatch = useAppDispatch()
  const {
    data,
    total,
    page,
    rowsPerPage,
    sortBy,
    sortOrder,
    filters
  } = useAppSelector(selectAssemblies)

  useEffect(() => {
    dispatch(fetchAssemblies())
  }, [dispatch, page, rowsPerPage, sortBy, sortOrder, filters])

  const handlePageChange = (_: unknown, newPage: number) => {
    dispatch(fetchAssemblies({ page: newPage }))
  }

  const handleRowsPerPageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(fetchAssemblies({ rowsPerPage: parseInt(e.target.value, 10), page: 0 }))
  }

  const handleSort = (field: string) => {
    const isAsc = sortBy === field && sortOrder === "asc"
    dispatch(fetchAssemblies({ sortBy: field, sortOrder: isAsc ? "desc" : "asc" }))
  }

  const handleFilterChange = (key: string, value: string | Dayjs | null) => {
    dispatch(fetchAssemblies({
      filters: {
        ...filters,
        [key]: value instanceof dayjs ? value.toISOString() : value
      },
      page: 0
    }))
  }

  return (
    <Box p={2}>
      <Grid container spacing={2} mb={2}>
        <Grid item xs={2}>
          <DatePicker
            label="From"
            value={filters.from ? dayjs(filters.from) : null}
            onChange={(value) => handleFilterChange("from", value)}
          />
        </Grid>
        <Grid item xs={2}>
          <DatePicker
            label="To"
            value={filters.to ? dayjs(filters.to) : null}
            onChange={(value) => handleFilterChange("to", value)}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            label="Assembler"
            value={filters.assembler || ""}
            onChange={(e) => handleFilterChange("assembler", e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            label="Model"
            value={filters.model || ""}
            onChange={(e) => handleFilterChange("model", e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={2}>
          <FormControl fullWidth>
            <InputLabel>Status</InputLabel>
            <Select
              label="Status"
              value={filters.status || ""}
              onChange={(e) => handleFilterChange("status", e.target.value)}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="pending">Pending</MenuItem>
              <MenuItem value="in_progress">In Progress</MenuItem>
              <MenuItem value="completed">Completed</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>
              <TableSortLabel
                active={sortBy === "date"}
                direction={sortBy === "date" ? sortOrder : "asc"}
                onClick={() => handleSort("date")}
              >
                Date
              </TableSortLabel>
            </TableCell>
            <TableCell>
              <TableSortLabel
                active={sortBy === "assembler"}
                direction={sortBy === "assembler" ? sortOrder : "asc"}
                onClick={() => handleSort("assembler")}
              >
                Assembler
              </TableSortLabel>
            </TableCell>
            <TableCell>
              <TableSortLabel
                active={sortBy === "model"}
                direction={sortBy === "model" ? sortOrder : "asc"}
                onClick={() => handleSort("model")}
              >
                Model
              </TableSortLabel>
            </TableCell>
            <TableCell>
              <TableSortLabel
                active={sortBy === "status"}
                direction={sortBy === "status" ? sortOrder : "asc"}
                onClick={() => handleSort("status")}
              >
                Status
              </TableSortLabel>
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((assembly) => (
            <TableRow key={assembly.id}>
              <TableCell>{dayjs(assembly.date).format("YYYY-MM-DD")}</TableCell>
              <TableCell>{assembly.assembler}</TableCell>
              <TableCell>{assembly.model}</TableCell>
              <TableCell>{assembly.status}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={handlePageChange}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={handleRowsPerPageChange}
      />
    </Box>
  )
}
