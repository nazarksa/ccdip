const platformAreas = [
  'Project 360',
  'Dependency graph',
  'Schedule intelligence',
  'Risk and scenarios',
  'Contracts and supply chain',
  'Document intelligence',
]

export function FoundationPage() {
  return (
    <section>
      <p className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-400">
        Saudi construction intelligence
      </p>
      <h1 className="mt-3 max-w-4xl text-4xl font-semibold tracking-tight sm:text-5xl">
        Causality and dependency intelligence platform
      </h1>
      <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-400">
        The application shell is ready. Business capabilities will be delivered as governed,
        independently testable modules.
      </p>
      <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {platformAreas.map((area) => (
          <div key={area} className="rounded-lg border border-slate-800 bg-slate-900 p-5">
            <p className="font-medium">{area}</p>
            <p className="mt-2 text-sm text-slate-500">Module boundary reserved</p>
          </div>
        ))}
      </div>
    </section>
  )
}
