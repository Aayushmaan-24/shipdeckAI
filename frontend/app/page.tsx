export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2 bg-slate-950 text-white">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-6xl font-bold">
          Welcome to <span className="text-blue-600">ShipDeck</span>
        </h1>
        <p className="mt-3 text-2xl">
          Ship your idea faster. From code to deck in minutes.
        </p>
        <div className="flex flex-wrap items-center justify-around max-w-4xl mt-6 sm:w-full">
          <button className="p-6 mt-6 text-left border w-96 rounded-xl hover:text-blue-600 focus:text-blue-600">
            <h3 className="text-2xl font-bold">Connect GitHub &rarr;</h3>
            <p className="mt-4 text-xl">
              Turn your repository into a pitch deck instantly.
            </p>
          </button>
        </div>
      </main>
    </div>
  );
}
