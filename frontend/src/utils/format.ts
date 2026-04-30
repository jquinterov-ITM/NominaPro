function normalizeNumericString(input: number | string): string {
  const s = String(input).trim()
  if (!s) return ''

  // remove spaces
  let str = s.replace(/\s+/g, '')
  const hasDot = str.indexOf('.') >= 0
  const hasComma = str.indexOf(',') >= 0

  if (hasDot && hasComma) {
    // both present: the last occurrence is the decimal separator
    const lastDot = str.lastIndexOf('.')
    const lastComma = str.lastIndexOf(',')
    const decimalSep = lastDot > lastComma ? '.' : ','
    const thousandsSep = decimalSep === '.' ? ',' : '.'
    // remove thousands separators
    str = str.split(thousandsSep).join('')
    // replace decimal separator with dot
    if (decimalSep === ',') str = str.replace(',', '.')
    return str
  }

  if (hasComma && !hasDot) {
    // only comma present: decide if decimal (e.g., 1.000.000,00) or thousands
    // if comma followed by 1-2 digits at the end => decimal
    if (/,[0-9]{1,2}$/.test(str)) {
      return str.replace(/\./g, '').replace(',', '.')
    }
    // otherwise treat comma as thousands sep
    return str.replace(/,/g, '')
  }

  if (hasDot && !hasComma) {
    // only dot present: if dot followed by 1-2 digits at end => decimal
    if (/\.[0-9]{1,2}$/.test(str)) {
      return str.replace(/,/g, '')
    }
    // otherwise treat dot as thousands sep
    return str.replace(/\./g, '')
  }

  return str
}

export function formatCurrency(value: number | string | null | undefined): string {
  if (value === null || value === undefined || value === '') return '-'

  const normalized = typeof value === 'number' ? String(value) : normalizeNumericString(value)
  const num = Number(normalized)
  if (Number.isNaN(num)) return '-'

  const hasDecimals = Math.abs(num % 1) > 0
  const formatter = new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: hasDecimals ? 2 : 0,
    maximumFractionDigits: hasDecimals ? 2 : 0
  })

  return `$ ${formatter.format(num)}`
}

export function normalizeForApi(value: number | string | null | undefined): string {
  if (value === null || value === undefined || value === '') return ''
  const normalized = typeof value === 'number' ? String(value) : normalizeNumericString(value)
  return normalized
}

