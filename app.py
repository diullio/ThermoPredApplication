import streamlit as st
from streamlit_ketcher import st_ketcher
from streamlit_navigation_bar import st_navbar #referencia https://github.com/gabrieltempass/streamlit-navigation-bar/wiki/Examples
from Thermopred.Enthalpie import EnthalpieEnergy
from Thermopred.GibbsEnergy import GibbsFreeEnergy
from rdkit import Chem


import texts

class FrontEnd:
    def __init__(self) -> None:
        self.backend = BackEnd()
    
    def main(self):
        navbar = self.navbar()
        
        if navbar == 'Thermopred':
            self.header_predictor()            
            molecule = st.text_input("Molecule",'CCO')
            try:
                smile_code = BackEnd.canonicalizeSmiles(st_ketcher(molecule))
                st.markdown(f"Canonical Smiles: ``{smile_code}``")
                self.body_predictor(smile_code)
            except:
                st.warning('Invalid molecule, please enter a valid Smiles.', icon="⚠️")
        
        elif navbar == 'Home':
            st.markdown(texts.home1(),unsafe_allow_html=True)
        
        elif navbar == 'About':
            st.markdown(texts.about1(),unsafe_allow_html=True)
    
    def header_predictor(self):
        st.markdown('## Thermopred')
        st.markdown(f"AI-Enhanced Quantum Chemistry Dataset for Thermochemical Properties of API-Like Compounds and Their Degradants")
        st.markdown(f"https://github.com/jeffrichardchemistry/thermopred")

    def body_predictor(self,smiles:list):        
        if st.button('Make Prediction'):
            try:
                with st.spinner("Calculating... Please, wait."):
                    results = self.backend.run_predictions(smiles)
                st.table(results)
            except:
                st.warning('Invalid molecule, please enter a valid Smiles.', icon="⚠️")

    def navbar(self):
        st.set_page_config(page_title="ThermoPred",
                           page_icon="🧪",
                           initial_sidebar_state="collapsed")
        options = {"show_menu": True,
                   "show_sidebar": False}
        pages = ["Thermopred"]
        #parent_dir = os.path.dirname(os.path.abspath(__file__))
        #logo_path = os.path.join(parent_dir, "figs/cubes.svg")
        styles = {
                "nav": {
                    "background-color": "royalblue",
                    #"justify-content": "left",
                },
                "img": {
                    "padding-right": "14px",
                },
                "span": {
                    "color": "white",
                    "padding": "14px",
                },
                "active": {
                    "background-color": "white",
                    "color": "var(--text-color)",
                    "font-weight": "normal",
                    "padding": "14px",
                }
            }
        page = st_navbar(pages,
                         options=options,
                         #logo_path=logo_path,
                         styles=styles
                         )
        return page


class BackEnd:
    def __init__(self) -> None:
        self.ee = EnthalpieEnergy()
        self.gfe = GibbsFreeEnergy()

    def run_predictions(self, smiles: str):
        results = []
        smiles_list = smiles.split('.')
        for s in smiles_list:
            try:
                result_enthalpie = self.ee.predict(s)
                result_gibbs = self.gfe.predict(smiles=s)
                results.append({
                    "SMILES": s,
                    "ΔH (Enthalpia)": result_enthalpie,
                    "ΔG (Gibbs Free Energy)": result_gibbs
                })
            except Exception as e:
                results.append({
                    "SMILES": s,
                    "ΔH (Enthalpia)": "Erro",
                    "ΔG (Gibbs Free Energy)": "Erro"
                })
        return results

    @staticmethod
    def canonicalizeSmiles(smiles:str):
        return Chem.MolToSmiles(Chem.MolFromSmiles(smiles),isomericSmiles=False)

if __name__ == '__main__':
    app = FrontEnd()
    app.main()