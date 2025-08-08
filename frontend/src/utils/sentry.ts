// frontend/src/utils/sentry.ts
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  release: process.env.REACT_APP_SENTRY_RELEASE,
  environment: process.env.NODE_ENV,
  integrations: [new BrowserTracing()],
  tracesSampleRate: 1.0
});

export default Sentry;
